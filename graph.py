import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator
import mplfinance as mpf
from setups import check_setups

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
    data.set_index('time', inplace=True)
    
    # Obter a data de três meses atrás
    tree_months_ago = pd.Timestamp.now() - pd.DateOffset(months=3)

    # Filtrar o DataFrame para incluir apenas os dados dos últimos 03 meses
    data_last_3_months = data.loc[tree_months_ago:]

    # Configurar o estilo dos candles
    mc = mpf.make_marketcolors(up='g', down='r', edge='i', wick='i', volume='in', ohlc='i')
    s = mpf.make_mpf_style(marketcolors=mc)

    add_plot = [
        mpf.make_addplot(data_last_3_months['EMA9'], color='green', width=0.5, label='Média exp 9'),
        mpf.make_addplot(data_last_3_months['SMA21'], color='yellow', width=1, label='Média arit. 21'),
        mpf.make_addplot(data_last_3_months['SMA80'], color='red', width=1.5, label='Média arit. 80'),
        mpf.make_addplot(data_last_3_months['SMA200'], color='blue', width=2, label='Média arit. 200')
    ]

    # Plotar os dados com candles
    fig, axlist = mpf.plot(data_last_3_months,
              type = 'candle', 
              style = s, 
              volume = False,
              addplot = add_plot, 
              title = symbol, 
              ylabel ='Preço',
              returnfig=True
              )
    
    ax = axlist[0]  # Pega o eixo principal do gráfico

    if (data['setup_9_1_buy'].iloc[len(data) - 1] or data['setup_9_2_buy'].iloc[len(data) - 1] or data['setup_9_3_buy'].iloc[len(data) - 1] or data['setup_PC_buy'].iloc[len(data) - 1]):
        max_price = data['high'].iloc[len(data) - 1]
        ax.hlines(max_price, xmin=len(data_last_3_months)-1, xmax=len(data_last_3_months), colors='limegreen', linestyles='dashed', linewidth=2, label='Entrada COMPRA')
    if (data['setup_9_1_sell'].iloc[len(data) - 1] or data['setup_9_2_sell'].iloc[len(data) - 1] or data['setup_9_3_sell'].iloc[len(data) - 1] or data['setup_PC_buy'].iloc[len(data) - 1]):
        min_price = data['low'].iloc[len(data) - 1]
        ax.hlines(min_price, xmin=len(data_last_3_months)-1, xmax=len(data_last_3_months), colors='limegreen', linewidth=2, label='Entrada VENDA')

    textstr = 'Tendência: ' + trend_result + '\n' + check_setups(data) + '\nIV Rank: ' + '\nIV Percentil: ' + '\nBeta: '
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8, verticalalignment='top', bbox=props)

    plt.show()