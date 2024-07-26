import MetaTrader5 as mt5
from symbols import get_candles, get_symbols_list
from moving_averages import analyze_trend

# Inicializar o MetaTrader 5
if not mt5.initialize():
    print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
    mt5.shutdown()
    exit()

# Verificar se o login foi bem-sucedido
account_info = mt5.account_info()
if account_info is None:
    print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
    mt5.shutdown()
    exit()
else:
    print(f"Login bem-sucedido: {account_info}")

# Exibir candles
symbol = 'AZUL4'
data = get_candles(symbol)
analyze_trend(data, symbol)
#print(data)
indices = get_symbols_list()
print(indices)

mt5.shutdown()