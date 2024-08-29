from datetime import datetime
import pytz
import MetaTrader5 as mt5

def get_options_list(symbol):
    
    symbol_options = symbol[:-1]
    ru_symbols=mt5.symbols_get(symbol_options)
    print(len(ru_symbols))
    for s in ru_symbols:
        print(s.name)
    print()

def get_options_info(symbol):

    symbol_info=mt5.symbol_info(symbol)
    
    return {
    "strike": symbol_info.option_strike,
    "bid": symbol_info.bid,
    "ask": symbol_info.ask,
    "expiration_time": symbol_info.expiration_time
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

def get_expiration_time(option):

    expiration_time = get_options_info(option)['expiration_time']
    utc = pytz.UTC
    expiration_date = datetime.fromtimestamp(expiration_time, tz=utc)
    current_date = datetime.now(tz=utc)
    difference_in_days = (expiration_date - current_date).days
    days_without_operation = difference_in_days % 7
    difference_in_years = (20) / 252

    return difference_in_years