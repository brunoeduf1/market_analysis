import numpy as np
import pandas as pd

def calcular_iv_rank(df_iv):
    """
    Calcula o IV Rank de uma série temporal de volatilidade implícita.

    Parâmetros:
    df_iv (pd.DataFrame): DataFrame contendo a série temporal de volatilidade implícita com uma coluna 'iv'.

    Retorna:
    float: O valor do IV Rank.
    """
    iv_atual = df_iv['iv'].iloc[-1]
    iv_min = df_iv['iv'].min()
    iv_max = df_iv['iv'].max()
    iv_rank = (iv_atual - iv_min) / (iv_max - iv_min) * 100
    return iv_rank

def calcular_iv_percentil(df_iv):
    """
    Calcula o IV Percentil de uma série temporal de volatilidade implícita.

    Parâmetros:
    df_iv (pd.DataFrame): DataFrame contendo a série temporal de volatilidade implícita com uma coluna 'iv'.

    Retorna:
    float: O valor do IV Percentil.
    """
    iv_atual = df_iv['iv'].iloc[-1]
    iv_percentil = (df_iv['iv'] <= iv_atual).sum() / len(df_iv) * 100
    return iv_percentil

def gerar_dados_iv():
    """
    Gera um DataFrame de exemplo com dados de volatilidade implícita.

    Retorna:
    pd.DataFrame: DataFrame contendo a série temporal de volatilidade implícita.
    """
    iv_data = {
        'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'iv': np.random.uniform(0.2, 0.5, 100)  # Valores de IV aleatórios entre 0.2 e 0.5
    }
    df_iv = pd.DataFrame(iv_data)
    return df_iv