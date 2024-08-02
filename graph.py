import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator
import mplfinance as mpf
from setups import check_setups
from services import get_symbol_data
from indicators import get_iv_1y_rank, get_iv_1y_percentile, get_iv_current

def analyze_trend(data):

    # Garantir que os dados estejam ordenados por data
    data.sort_values('time', inplace=True)
    data.set_index('time', inplace=True)

    # Calcular médias móveis aritiméticas de 21, 80 e 200 períodos
    data['SMA21'] = SMAIndicator(data['close'], window=21).sma_indicator()
    data['SMA80'] = SMAIndicator(data['close'], window=80).sma_indicator()
    data['SMA200'] = SMAIndicator(data['close'], window=200).sma_indicator()

    # Calcular média exponencial de 9 períodos
    data['EMA9'] =  EMAIndicator(data['close'], window=9).ema_indicator()

    # Calcular a media de 21 no volume
    data['SMA21_vol'] = SMAIndicator(data['real_volume'], window=21).sma_indicator()

    # Função para determinar a tendência
    def determine_trend(df):
        if df['close'].iloc[-1] > df['EMA9'].iloc[-1] > df['SMA21'].iloc[-1] > df['SMA80'].iloc[-1]:
            return 'ALTA'
        elif df['close'].iloc[-1] < df['EMA9'].iloc[-1] < df['SMA21'].iloc[-1] < df['SMA80'].iloc[-1]:
            return 'BAIXA'
        else:
            return 'ACUMULAÇÃO'

    trend_result = determine_trend(data)

    return trend_result

def plot_graph(symbol, data, trend_result):
    # Obter a data de três meses atrás
    tree_months_ago = pd.Timestamp.now() - pd.DateOffset(months=3)

    # Filtrar o DataFrame para incluir apenas os dados dos últimos 03 meses
    data_last_3_months = data.loc[tree_months_ago:]

    # Configurar o estilo dos candles
    mc = mpf.make_marketcolors(up='g', down='r', edge='i', wick='i', volume='in', ohlc='i')
    s = mpf.make_mpf_style(marketcolors=mc, facecolor='#1C1C1C', rc={'text.color': 'white', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white'})  # Fundo grafite e texto branco

    add_plot = [
        mpf.make_addplot(data_last_3_months['EMA9'], color='green', width=0.5),
        mpf.make_addplot(data_last_3_months['SMA21'], color='yellow', width=1),
        mpf.make_addplot(data_last_3_months['SMA80'], color='red', width=1.5),
        mpf.make_addplot(data_last_3_months['SMA200'], color='blue', width=2),
        mpf.make_addplot(data_last_3_months['SMA21_vol'], panel=1, color='yellow', width=1)
    ]

    # Verificar se a coluna "real_volume" está presente no DataFrame
    if 'real_volume' in data_last_3_months.columns:
        volume = True
        ylabel_lower = 'Volume'
        data_last_3_months.rename(columns={'real_volume': 'volume'}, inplace=True)  # Renomear a coluna para 'volume' para compatibilidade com mplfinance
    else:
        volume = False
        ylabel_lower = None

    # Plotar os dados com candles e volume (se disponível)
    fig, axlist = mpf.plot(data_last_3_months,
              type='candle', 
              style=s, 
              volume=volume,  # Adicionar gráfico de volume se disponível
              addplot=add_plot, 
              title=symbol, 
              ylabel='Preço',
              ylabel_lower=ylabel_lower,  # Rótulo para o gráfico de volume se disponível
              returnfig=True
              )
    
    fig.patch.set_facecolor('#1C1C1C')
    ax = axlist[0]  # Pega o eixo principal do gráfico

    # Adicionar setas para compra e venda
    if (data['setup_9_1_buy'].iloc[-1] or data['setup_9_2_buy'].iloc[-1] or data['setup_9_3_buy'].iloc[-1] or data['setup_PC_buy'].iloc[-1]):
        max_price = data['high'].iloc[-1]
        ax.annotate('', xy=(len(data_last_3_months)-1, max_price), xytext=(len(data_last_3_months)-1, max_price + (max_price * 0.02)),
                    arrowprops=dict(facecolor='limegreen', shrink=0.05, width=2, headwidth=8), label='Entrada COMPRA')

    if (data['setup_9_1_sell'].iloc[-1] or data['setup_9_2_sell'].iloc[-1] or data['setup_9_3_sell'].iloc[-1] or data['setup_PC_sell'].iloc[-1]):
        min_price = data['low'].iloc[-1]
        ax.annotate('', xy=(len(data_last_3_months)-1, min_price), xytext=(len(data_last_3_months)-1, min_price - (min_price * 0.02)),
                    arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8), label='Entrada VENDA')
    
    stocks = get_symbol_data()
    iv_rank = get_iv_1y_rank(stocks, symbol)
    iv_percentil = get_iv_1y_percentile(stocks, symbol)
    iv_current = get_iv_current(stocks, symbol)

    textstr = (
        'Tendência: ' + trend_result + '\n' +
        check_setups(data) + '\n' +
        'IV Rank: ' + str(iv_rank) + '\n' +
        'IV Percentil: ' + str(iv_percentil) +'\n' +
        'Vol Implicita: ' + str(iv_current)
    )

    # Adicionar um novo eixo para o texto
    ax_text = fig.add_axes([0.05, 0.8, 0.2, 0.2], frameon=False)  # [left, bottom, width, height]
    ax_text.axis('off')  # Desativar os eixos

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax_text.text(0, 0.7, textstr, transform=ax_text.transAxes, fontsize=8, verticalalignment='center', bbox=props, ha='left')

    plt.show()