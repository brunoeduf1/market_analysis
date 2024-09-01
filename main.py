import MetaTrader5 as mt5
from flow_analysis.players import get_players_positions
from options.greeks import calc_greeks
from options.options_fair_price import calc_historic_vol, get_option_fair_price, get_symbol_price
from stocks.symbols_analysis import get_candles, print_symbol_analisys, print_analisys_result, plot_symbol_graph
from machine_learning.predictor import run_machine_learning
from options.options_info import get_options_list, get_options_info
from configs.Initialize_mt5 import initialize

initialize()

#get_options_list('PETR4')
#plot_symbol_graph('VIVT3')
#print_analisys_result()
#run_machine_learning('VALE3')
#print(get_candles('PETR4'))
#print_symbol_analisys('GOLL4')
#get_players_positions('PETR4')

#price = get_option_fair_price('PETR4','PETRU416')
#print(price)

greeks = calc_greeks('PETR4','PETRU416')
print(greeks)

mt5.shutdown()