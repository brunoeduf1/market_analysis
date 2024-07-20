import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
from candles import getCandles

# Ler credenciais
try:
    login, password = open('_credentials').read().split()
except Exception as e:
    print(f"Erro ao ler o arquivo de credenciais: {e}")
    exit()

# Inicializar o MetaTrader 5
if not mt5.initialize():
    print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
    quit()

# Verificar se o login foi bem-sucedido
account_info = mt5.account_info()
if account_info is None:
    print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
    mt5.shutdown()
    exit()
else:
    print(f"Login bem-sucedido: {account_info}")

# Print candles
candles = getCandles('PETR4')
print(candles.head(10))