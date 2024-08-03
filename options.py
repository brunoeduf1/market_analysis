import MetaTrader5 as mt5

def get_options_list(symbol):
    
    symbol_options = symbol[:-1]
    ru_symbols=mt5.symbols_get(symbol_options)
    print('len(*PETR4*): ', len(ru_symbols))
    for s in ru_symbols:
        print(s.name)
    print()
    