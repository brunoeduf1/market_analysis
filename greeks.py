import MetaTrader5 as mt5
import mibian

def get_market_data(symbol):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"Não foi possível obter dados para o símbolo {symbol}")
        return None
    return tick.last

def calculate_delta(option_data):
    return mibian.BS(option_data, callPrice=option_data['option_price']).delta

def calculate_gamma(option_data):
    return mibian.BS(option_data, callPrice=option_data['option_price']).gamma

def calculate_vega(option_data):
    return mibian.BS(option_data, callPrice=option_data['option_price']).vega

def calculate_theta(option_data):
    return mibian.BS(option_data, callPrice=option_data['option_price']).theta

def calculate_rho(option_data):
    return mibian.BS(option_data, callPrice=option_data['option_price']).rho