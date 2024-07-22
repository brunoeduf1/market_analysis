import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator

def analyze_trend(data, ativo):

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

    # Obter a data de um ano atrás
    one_year_ago = pd.Timestamp.now() - pd.DateOffset(years=1)

    # Filtrar o DataFrame para incluir apenas os dados dos últimos 12 meses
    data_last_year = data.loc[one_year_ago:]

    # Visualizar os dados
    plt.figure(figsize=(14, 7))
    plt.plot(data_last_year['close'], label='Preço de Fechamento')
    plt.plot(data_last_year['EMA9'], label='Média exp 9')
    plt.plot(data_last_year['SMA21'], label='Média arit. 21')
    plt.plot(data_last_year['SMA80'], label='Média arit. 80')
    plt.plot(data_last_year['SMA200'], label='Média arit. 200')
    plt.title('Tendência de ' + tendencia  + ' do ativo ' + ativo)
    plt.legend()
    plt.show()

    return tendencia
