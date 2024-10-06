from datetime import datetime
from numpy import double
import pytz
import MetaTrader5 as mt5
from stocks.symbols_analysis import get_candles

def get_options_list(option, expiration):

    if len(option) == 5:
        symbol_options = option[:-1]
    elif len(option) == 6:
        symbol_options = option[:-2]
    else:
        print('Código inválido')
        return []

    ru_symbols = mt5.symbols_get(symbol_options)
    
    if not ru_symbols:
        print(f"Nenhum símbolo encontrado para {symbol_options}")
        return []

    options_list = []

    for option in ru_symbols:
        if len(option.name) >= 5 and option.name[4] == expiration:
            if 'W' not in option.name[5:]:
                options_list.append(option)

    return options_list

def get_options_by_price(symbol, expiration, min_price, max_price):

    options_list = get_options_list(symbol, expiration)
    if not options_list:
        return []
    
    options = []

    for option in options_list:
        try:
            price = double(get_symbol_price(option.name))
            if double(min_price) <= price <= double(max_price):
                options.append(option)

        except IndexError:
            print(f"Índice fora do limite ao acessar o preço para a opção {option.name}")
        
        except ValueError:
            print(f"Erro ao converter o preço para a opção {option.name}: {price}")
        
        except Exception as e:
            print(f"Erro ao obter o preço para a opção {option.name}: {e}")
    
    return options


def get_options_info(symbol):
    symbol_info=mt5.symbol_info(symbol)
    
    return {
    "strike": symbol_info.option_strike,
    "bid": symbol_info.bid,
    "ask": symbol_info.ask,
    "expiration_time": symbol_info.expiration_time,
    "name": symbol_info.name
    }

def identify_option_type(option):

    if len(option) < 5:
        return "Código inválido"

    letter_type = option[4].upper()

    if letter_type in "ABCDEFGHIJKL":
        return "call"
    elif letter_type in "MNOPQRSTUVWX":
        return "put"
    else:
        return "Código inválido"

def identify_option_type_by_expiration(expiration):

    if expiration in "ABCDEFGHIJKL":
        return "call"
    elif expiration in "MNOPQRSTUVWX":
        return "put"
    else:
        return "Código inválido"

def get_expiration_time(option):
    days_to_expire = get_expiration_days_without_weekend(option)
    difference_in_years = days_to_expire / 252

    return difference_in_years

def get_expiration_days_without_weekend(option):
    expiration_time = get_options_info(option)['expiration_time']
    utc = pytz.UTC
    expiration_date = datetime.fromtimestamp(expiration_time, tz=utc)
    current_date = datetime.now(tz=utc)
    difference_in_days = (expiration_date - current_date).days
    days_without_operation = difference_in_days % 7
    days_to_expire = difference_in_days - days_without_operation

    return days_to_expire

def get_expiration_days(option):
    expiration_time = get_options_info(option)['expiration_time']
    utc = pytz.UTC
    expiration_date = datetime.fromtimestamp(expiration_time, tz=utc)
    current_date = datetime.now(tz=utc)

    return (expiration_date - current_date).days

def get_symbol_price(symbol):
    stocks = get_candles(symbol)
    if stocks.empty:
        return[]
    
    last_strike = stocks['close'].iloc[-1]

    return last_strike

def get_ATM_options(symbol, expiration):
    
    symbol_price = get_symbol_price(symbol)
    options_list = get_options_list(symbol, expiration)
    options_list_info = []

    for option in options_list:
        options_list_info.append(get_options_info(option.name))

    options_below = sorted(
        (option for option in options_list_info if option['strike'] <= symbol_price),
        key=lambda option: abs(option['strike'] - symbol_price)
    )

    strikes_below = [option['strike'] for option in options_below[:2]]
    options_names_below = [option['name'] for option in options_below[:2]]

    # Ordenar opções acima do preço do ativo pela diferença absoluta do strike para o preço do ativo
    options_above = sorted(
        (option for option in options_list_info if option['strike'] > symbol_price),
        key=lambda option: abs(option['strike'] - symbol_price)
    )

    # Selecionar os dois strikes acima mais próximos
    strikes_above = [option['strike'] for option in options_above[:2]]
    options_names_above = [option['name'] for option in options_above[:2]]
    
    return {
        'options_names_below': options_names_below,
        'strikes_below': strikes_below,
        'options_names_above': options_names_above,
        'strikes_above': strikes_above
    }

def get_ITM_options(symbol, expiration):

    option_type = identify_option_type_by_expiration(expiration)

    symbol_price = get_symbol_price(symbol)
    options_list = get_options_list(symbol, expiration)
    
    options_list_info = []

    for option in options_list:
        options_list_info.append(get_options_info(option.name))
    
    itm_options = []

    if option_type == 'call':
        itm_options = [
            option for option in options_list_info 
            if option['strike'] <= symbol_price
        ]
        if itm_options:
            itm_options_sorted = sorted(itm_options, key=lambda x: x['strike'], reverse=True)

    if option_type == 'put':
        itm_options = [
            option for option in options_list_info 
            if option['strike'] >= symbol_price
        ]
        if itm_options:
            itm_options_sorted = sorted(itm_options, key=lambda x: x['strike'])
    
    if itm_options_sorted:
        itm_options_sorted = itm_options_sorted[1:]
    
    top_10_itm_options = itm_options_sorted[:10]

    for option in top_10_itm_options:
        print(f"Option Name: {option['name']}, Strike: {option['strike']}")
    
    return top_10_itm_options

def get_OTM_options(symbol, expiration):

    option_type = identify_option_type_by_expiration(expiration)

    symbol_price = get_symbol_price(symbol)
    options_list = get_options_list(symbol, expiration)
    
    options_list_info = []

    for option in options_list:
        options_list_info.append(get_options_info(option.name))
    
    otm_options = []
    otm_options_sorted = []

    if option_type == 'call':
        otm_options = [
            option for option in options_list_info 
            if option['strike'] >= symbol_price
        ]
        if otm_options:
            otm_options_sorted = sorted(otm_options, key=lambda x: x['strike'])

    if option_type == 'put':
        otm_options = [
            option for option in options_list_info 
            if option['strike'] <= symbol_price
        ]
        if otm_options:
            otm_options_sorted = sorted(otm_options, key=lambda x: x['strike'], reverse=True)
    
    if otm_options_sorted:
        otm_options_sorted = otm_options_sorted[1:]

    top_10_otm_options = otm_options_sorted[:10]

    for option in top_10_otm_options:
        print(f"Option Name: {option['name']}, Strike: {option['strike']}")
    
    return top_10_otm_options