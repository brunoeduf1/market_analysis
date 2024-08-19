import numpy as np
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd

# Indicadores IV Rank, IV Percentil e Volatilidade Implicita

def get_iv_1y_rank(stocks, symbol):
    for stock in stocks:
        if stock.get('symbol') == symbol:
            return stock.get('iv_1y_rank')
    raise Exception(f"Símbolo {symbol} não encontrado")

def get_iv_1y_percentile(stocks, symbol):
    for stock in stocks:
        if stock.get('symbol') == symbol:
            return stock.get('iv_1y_percentile')
    raise Exception(f"Símbolo {symbol} não encontrado")

def get_iv_current(stocks, symbol):
    for stock in stocks:
        if stock.get('symbol') == symbol:
            return stock.get('iv_current')
    raise Exception(f"Símbolo {symbol} não encontrado")
