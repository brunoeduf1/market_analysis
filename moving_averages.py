import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator
import mplfinance as mpf
from setups import apply_setups, check_setups

def analyze_trend(data, symbol):

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
    def determinar_tendencia(df):
        if df['close'].iloc[-1] > df['EMA9'].iloc[-1] > df['SMA21'].iloc[-1] > df['SMA80'].iloc[-1]:
            return 'ALTA'
        elif df['close'].iloc[-1] < df['EMA9'].iloc[-1] < df['SMA21'].iloc[-1] < df['SMA80'].iloc[-1]:
            return 'BAIXA'
        else:
            return 'ACUMULAÇÃO'

    tendencia = determinar_tendencia(data)
    print(f"A tendência atual do ativo é: {tendencia}")

    # Analisar se acionou algum setup
    data = apply_setups(data)
    print(data[['setup_9_1_buy', 'setup_9_1_sell', 'setup_9_2_buy', 'setup_9_2_sell', 'setup_9_3_buy', 'setup_9_3_sell', 'setup_PC_buy', 'setup_PC_sell']])

    # Obter a data de um ano atrás
    one_year_ago = pd.Timestamp.now() - pd.DateOffset(years=1)

    # Filtrar o DataFrame para incluir apenas os dados dos últimos 12 meses
    data_last_year = data.loc[one_year_ago:]

    # Configurar o estilo dos candles
    mc = mpf.make_marketcolors(up='g', down='r', edge='i', wick='i', volume='in', ohlc='i')
    s = mpf.make_mpf_style(marketcolors=mc)

    add_plot = [
        mpf.make_addplot(data_last_year['EMA9'], color='green', width=0.5, label='Média exp 9'),
        mpf.make_addplot(data_last_year['SMA21'], color='yellow', width=1, label='Média arit. 21'),
        mpf.make_addplot(data_last_year['SMA80'], color='red', width=1.5, label='Média arit. 80'),
        mpf.make_addplot(data_last_year['SMA200'], color='blue', width=2, label='Média arit. 200')
    ]

    # Plotar os dados com candles
    fig, axlist = mpf.plot(data_last_year,
              type = 'candle', 
              style = s, 
              volume = False,
              addplot = add_plot, 
              title = symbol, 
              ylabel ='Preço',
              returnfig=True
              )
    
    ax = axlist[0]  # Pega o eixo principal do gráfico
    textstr = 'Tendência: ' + tendencia + '\n' + check_setups(data) + '\nIV Rank: ' + '\nIV Percentil: ' + '\nBeta: '
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8, verticalalignment='top', bbox=props)

    plt.show()

    return tendencia