import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

symbols_list = [
    'ABEV3', 'ALPA4', 'AMER3', 'ASAI3', 'AZUL4',
    'B3SA3', 'BAPC11', 'BBAS3', 'BBDC4', 'BBSE3',
    'BHIA3', 'BOVA11', 'BRAP4', 'BEEF3', 'BRFS3',
    'BRKM5', 'CIEL3', 'CMIG4', 'CPLE6', 'CSAN3',
    'CSNA3', 'CVCB3', 'CYRE3', 'DXCO3', 'ECOR3',
    'EGIE3', 'ELET3', 'EMBR3', 'ENEV3', 'EQTL3',
    'EZTC3', 'GGBR4', 'GOLL4', 'GOAU4', 'HAPV3',
    'HYPE3', 'IGTI11O', 'IRBR3', 'ITSA4', 'ITUB4',
    'JBSS3', 'JHSF3', 'KLBN11', 'LREN3', 'LWSA3',
    'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3',
    'PCAR3', 'PETR4', 'PETZ3', 'PRIO3', 'QUAL3',
    'RADL3', 'RAIL3', 'RAIZ4', 'RDOR3', 'RENT3',
    'RRRP3', 'SANB11', 'SBSP3', 'SLCE3', 'SOMA3',
    'SUZB3', 'TAEE11', 'TIMS3', 'UGPA3', 'USIM5',
    'VALE3', 'VBBR3', 'VIVT3', 'WEGE3'
]

def get_candles(symbol):

    # Obtém os dados das candles
    candles = mt5.copy_rates_range(
        symbol,
        mt5.TIMEFRAME_D1,
        datetime.today() - timedelta(days=548), # Um ano e meio atrás
        datetime.today(),
    )

    # Converte os dados para um DataFrame do Pandas
    df_candles = pd.DataFrame(candles)
    df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s')

    return df_candles

def get_symbols_list():
    return symbols_list
