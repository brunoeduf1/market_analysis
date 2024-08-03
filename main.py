import MetaTrader5 as mt5
from symbols import get_candles, get_symbols_list, process_symbol
from graph import analyze_trend, plot_graph
from setups import apply_setups
from services import get_symbol_data
from predictor import run_machine_learning
from options import get_options_list
from datetime import datetime

def initialize():
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

def plot_symbol_graph(symbol):
    data = get_candles(symbol)
    trend = analyze_trend(data)
    data = apply_setups(data)
    plot_graph(symbol, data, trend)

def print_analisys_result():
    # Analisar se acionou algum setup
    stocks = get_symbol_data()
    symbols = get_symbols_list()
    results = []

    for symbol in symbols:
        result = process_symbol(stocks, symbol)
        if result:
            results.append(result)

    # Ordenar os resultados pelo 'iv_percentile'
    results = sorted(results, key=lambda x: x['iv_percentile'])

    # Imprimir os resultados ordenados
    for result in results:
        # Concatena os setups ativos em uma string
        setups_str = ', '.join(result['setups'])
        
        print(
            f"{result['symbol']} - "
            f"{setups_str} - "
            f"IV Percentil: {result['iv_percentile']} - "
            f"IV Rank: {result['iv_rank']} - "
            f"Vol Implicita: {result['iv_current']}"
        )

initialize()

#get_options_list('PETR4')
#plot_symbol_graph('BBSE3')
print_analisys_result()
#run_machine_learning('AMER3')

mt5.shutdown()