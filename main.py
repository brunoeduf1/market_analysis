import MetaTrader5 as mt5
from symbols import get_candles, get_symbols_list, process_symbol
from graph import analyze_trend, plot_graph
from setups import apply_setups, check_setups

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

# Analisar se acionou algum setup
symbols = get_symbols_list()
for symbol in symbols:
    process_symbol(symbol)

symbol = 'BOVA11'
data = get_candles(symbol)
trend = analyze_trend(data)
data = apply_setups(data)

plot_graph(symbol, data, trend)

mt5.shutdown()