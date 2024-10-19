import MetaTrader5 as mt5
from flow_analysis.players import get_history_deals, get_history_orders, get_orders, get_players_positions
from options.greeks import calc_greeks
from options.options_fair_price import calc_exponential_historic_vol, calc_exponential_historic_vol2, calc_exponential_historic_vol3, calc_exponential_historic_vol4, calc_exponential_historic_vol5, calc_historic_vol, get_option_fair_price, get_symbol_price
from options.strategies import box_spread, broken_wing_butterfly, butterfly_spread, conversion_reversal, iron_condor, straddle_arbitrage, synthetic_arbitrage, tree_point_box
from stocks.symbols_analysis import get_candles, print_symbol_analisys, print_analisys_result, plot_symbol_graph
from machine_learning.predictor import run_machine_learning
from options.options_info import get_ATM_options, get_ITM_options, get_OTM_options, get_options_by_price, get_options_list, get_options_info
from configs.Initialize_mt5 import initialize
import argparse

initialize()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Chame funções do terminal.")
#     parser.add_argument("funcao", type=str, help="Nome da função a ser chamada")
#     parser.add_argument("args", nargs="*", help="Argumentos para a função")

#     args = parser.parse_args()

#     if args.funcao == "analisys":
#         print_analisys_result(*args.args)
    
#     if args.funcao == "candles":
#         print(get_candles(*args.args))
    
#     if args.funcao == "graph":
#         plot_symbol_graph(*args.args)

#     else:
#         print("Função não reconhecida.")

# python main.py print_analisys_result

plot_symbol_graph('ENEV3')
#run_machine_learning('VALE3')
#print_symbol_analisys('PETR4')
#print(get_option_fair_price('ABEV3','ABEVU135'))
#print(calc_greeks('ABEV3','ABEVU135'))
#get_players_positions('BBDCU158')
#get_history_deals('BOVAV119')
#get_history_orders('BOVAV119')
#get_orders('BOVAV119')
#print(get_options_info('BOVAV119'))

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

#tree_point_box('BOVA11','K', 'W')
#box_spread('BOVA11','K', 'W')
#broken_wing_butterfly('BOVA11','K')
#conversion_reversal('BOVA11','K', 'W')
#synthetic_arbitrage('BOVA11','K', 'W')
#iron_condor('BOVA11','K', 'W')

#butterfly_spread('VALE3','K')



mt5.shutdown()