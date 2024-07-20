import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def getCandles(ativo):

    # Obtém os dados das candles
    candles = mt5.copy_rates_range(
        ativo,
        mt5.TIMEFRAME_D1,
        datetime(2024, 7, 11),
        datetime.today(),
    )

    # Desconecta do MetaTrader 5
    mt5.shutdown()

    # Converte os dados para um DataFrame do Pandas
    df_candles = pd.DataFrame(candles)
    df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s')

    return df_candles