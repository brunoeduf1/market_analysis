import numpy as np
import pandas as pd

def get_iv_rank(df_iv):
    iv_atual = df_iv['iv'].iloc[-1]
    iv_min = df_iv['iv'].min()
    iv_max = df_iv['iv'].max()
    iv_rank = (iv_atual - iv_min) / (iv_max - iv_min) * 100
    return iv_rank

def get_iv_percentil(df_iv):
    iv_atual = df_iv['iv'].iloc[-1]
    iv_percentil = (df_iv['iv'] <= iv_atual).sum() / len(df_iv) * 100
    return iv_percentil

def gerar_dados_iv():
    iv_data = {
        'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'iv': np.random.uniform(0.2, 0.5, 100)  # Valores de IV aleatórios entre 0.2 e 0.5
    }
    df_iv = pd.DataFrame(iv_data)
    return df_iv