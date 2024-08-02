import MetaTrader5 as mt5
from symbols import get_candles, get_symbols_list, process_symbol
from graph import analyze_trend, plot_graph
from setups import apply_setups
from services import get_symbol_data
from predictor import get_historical_data, prepare_data, train_model, evaluate_model, predict_next_candle, build_model 

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
def run_machine_learning(symbol):
    timeframe = mt5.TIMEFRAME_D1
    num_candles = 1000

    data = get_historical_data(symbol, timeframe, num_candles)
    X_train, X_test, y_train, y_test, scaler_X, scaler_y = prepare_data(data)
    model = build_model(X_train.shape[1])
    model = train_model(model, X_train, y_train)
    evaluate_model(model, X_test, y_test)

    next_candle_prediction = predict_next_candle(model, X_train, scaler_X, scaler_y)
    print(f"Previsão do próximo candle:")
    print(f"Abertura: {next_candle_prediction[0]}")
    print(f"Máxima: {next_candle_prediction[1]}")
    print(f"Mínima: {next_candle_prediction[2]}")
    print(f"Fechamento: {next_candle_prediction[3]}")
    print(f"Volume: {next_candle_prediction[4]}")

initialize()

#plot_symbol_graph('BBSE3')
#print_analisys_result()
run_machine_learning('GGBR4')


mt5.shutdown()