import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator

def analyze_trend(data):

    # Garantir que os dados estejam ordenados por data
    data.sort_values('time', inplace=True)
    data.set_index('time', inplace=True)

    # Calcular médias móveis de 21, 80 e 200 períodos
    data['SMA21'] = SMAIndicator(data['close'], window=50).sma_indicator()
    data['SMA80'] = SMAIndicator(data['close'], window=200).sma_indicator()
    data['SMA200'] = SMAIndicator(data['close'], window=200).sma_indicator()

    # Calcular RSI de 9 períodos
    data['EMA'] = RSIIndicator(data['close'], window=9).rsi()

    # Função para determinar a tendência
    def determinar_tendencia(df):
        if df['close'].iloc[-1] > df['SMA21'].iloc[-1] > df['SMA80'].iloc[-1]:
            return 'Alta'
        elif df['close'].iloc[-1] < df['SMA21'].iloc[-1] < df['SMA80'].iloc[-1]:
            return 'Baixa'
        else:
            return 'Acumulação'

    tendencia = determinar_tendencia(data)
    print(f"A tendência atual do ativo é: {tendencia}")

    # Visualizar os dados
    plt.figure(figsize=(14, 7))
    plt.plot(data['close'], label='Preço de Fechamento')
    plt.plot(data['EMA'], label='EMA 9')
    plt.plot(data['SMA21'], label='SMA 21')
    plt.plot(data['SMA80'], label='SMA 80')
    plt.plot(data['SMA200'], label='SMA 200')
    plt.title('Tendência do Ativo')
    plt.legend()
    plt.show()

    return tendencia
