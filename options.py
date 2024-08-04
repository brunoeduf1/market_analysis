import MetaTrader5 as mt5

def get_options_list(symbol):
    
    symbol_options = symbol[:-1]
    ru_symbols=mt5.symbols_get(symbol_options)
    print('len(*PETR4*): ', len(ru_symbols))
    for s in ru_symbols:
        print(s.name)
    print()

def get_options_info(symbol):

    symbol_info=mt5.symbol_info(symbol)
    if symbol_info!=None:
        # display the terminal data 'as is'    
        print(symbol_info)
        print("EURJPY: spread =",symbol_info.spread,"  digits =",symbol_info.digits)
        # display symbol properties as a list
        symbol_info_dict = mt5.symbol_info(symbol)._asdict()
        for prop in symbol_info_dict:
            print("  {}={}".format(prop, symbol_info_dict[prop]))

def get_option_orders(option):
    orders=mt5.orders_get(symbol=option)
    if orders is None:
        print("No orders, error code={}".format(mt5.last_error()))
    else:
        print("Total orders:",len(orders))
        # display all active orders
        for order in orders:
            print(order)
    print()