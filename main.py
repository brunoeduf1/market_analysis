import MetaTrader5 as mt5
from flow_analysis.players import get_history_deals, get_players_positions
from options.greeks import calc_greeks
from options.options_fair_price import calc_exponential_historic_vol, calc_exponential_historic_vol2, calc_exponential_historic_vol3, calc_exponential_historic_vol4, calc_exponential_historic_vol5, calc_historic_vol, get_option_fair_price, get_symbol_price
from stocks.symbols_analysis import get_candles, print_symbol_analisys, print_analisys_result, plot_symbol_graph
from machine_learning.predictor import run_machine_learning
from options.options_info import get_ATM_options, get_ITM_options, get_OTM_options, get_options_by_price, get_options_list, get_options_info
from configs.Initialize_mt5 import initialize

initialize()

#plot_symbol_graph('ENEV3')
print_analisys_result()
#run_machine_learning('VALE3')
#print(get_candles('ENEV3'))
#print_symbol_analisys('BHIA3')
#print(get_option_fair_price('ABEV3','ABEVU135'))
#print(calc_greeks('ABEV3','ABEVU135'))
#get_players_positions('BBDCU158')
#get_history_deals('BBDCU158')
# options = get_options_by_price('ABEV3','U', 0.10, 0.50)
# for option in options:
#     print(option.name + ': ' + str(get_symbol_price(option.name)))

#print(get_ATM_options('ABEV3', 'U')['strikes_above'])
#print(get_ATM_options('ABEV3', 'U')['strikes_below'])

#get_ITM_options('ABEV3','I')
#get_OTM_options('ABEV3','U')

#print(calc_exponential_historic_vol5('BBDC4'))
# print(get_option_fair_price('ABEV3', 'ABEVI130'))
# print(calc_greeks('ABEV3','ABEVU135'))

mt5.shutdown()