import MetaTrader5 as mt5
from symbols import get_candles, get_symbols_list
from graph import analyze_trend, plot_graph
from setups import apply_setups, check_setups
from services import get_symbol_data

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
symbol = 'PETR4'
data = get_candles(symbol)
trend = analyze_trend(data)

# Analisar se acionou algum setup
data = apply_setups(data)
#print(data[['setup_9_1_buy', 'setup_9_1_sell', 'setup_9_2_buy', 'setup_9_2_sell', 'setup_9_3_buy', 'setup_9_3_sell', 'setup_PC_buy', 'setup_PC_sell']])

if (data['setup_9_1_buy'].iloc[len(data)-1] or data['setup_9_1_sell'].iloc[len(data)-1] or
    data['setup_9_2_buy'].iloc[len(data)-1] or data['setup_9_2_sell'].iloc[len(data)-1] or
    data['setup_9_3_buy'].iloc[len(data)-1] or data['setup_9_3_sell'].iloc[len(data)-1] or
    data['setup_PC_buy'].iloc[len(data)-1] or data['setup_PC_sell'].iloc[len(data)-1]):
    print(symbol + ' ' + check_setups(data))

plot_graph(symbol, data, trend)

#print(data)
indices = get_symbols_list()
#print(indices)

mt5.shutdown()