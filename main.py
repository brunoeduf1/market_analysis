import MetaTrader5 as mt5
from symbols_analysis import get_candles, print_symbol_analisys, print_analisys_result, plot_symbol_graph
from predictor import run_machine_learning
from options import get_options_list, get_options_info
from Initialize_mt5 import initialize

initialize()

#get_options_list('PETR4')
#plot_symbol_graph('VIVT3')
print_analisys_result()
#run_machine_learning('VALE3')
#print(get_candles('PETR4'))
#option_data = get_options_info('PETRU332')
#get_option_orders('PETRH393')
#print_symbol_analisys('VIVT3')

mt5.shutdown()