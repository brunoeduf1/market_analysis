import MetaTrader5 as mt5

## Revisar

def get_options_list(symbol):
    
    symbol_options = symbol[:-1]
    ru_symbols=mt5.symbols_get(symbol_options)
    print(len(ru_symbols))
    for s in ru_symbols:
        print(s.name)
    print()

def get_options_info(symbol):

    symbol_info=mt5.symbol_info(symbol)
    if symbol_info!=None:
        print(
            'Strike: ' + str(symbol_info.option_strike) + '\n' +
            'Bid: ' + str(symbol_info.bid) + '\n' +
            'Ask: ' + str(symbol_info.ask)
        )
    
    return {
    "Strike": symbol_info.option_strike,
    "Bid": symbol_info.bid,
    "Ask": symbol_info.ask
    }


def identify_option_type(option_code):

    if len(option_code) < 5:
        return "Código inválido"

    letter_type = option_code[4].upper()

    if letter_type in "ABCDEFGHIJKL":
        return "call"
    elif letter_type in "MNOPQRSTUVWX":
        return "put"
    else:
        return "Código inválido"