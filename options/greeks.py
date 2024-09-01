import mibian
from options.options_fair_price import calc_historic_vol, get_interest_rate, get_symbol_price
from options.options_info import get_expiration_days, get_options_info, identify_option_type

def calc_greeks(symbol, option):
    symbol_price = get_symbol_price(symbol)
    option_info = get_options_info(option)
    option_strike = option_info['strike']
    option_price = get_symbol_price(option)
    vol = calc_historic_vol(symbol)*100
    r = get_interest_rate()*100
    exp_time = get_expiration_days(option)

    option_type = identify_option_type(option)
    get_greeks = mibian.BS([symbol_price, option_strike, r, exp_time], volatility=vol)

    if(option_type == 'put'):
        impliedVolatility = mibian.BS([symbol_price, option_strike, r, exp_time], putPrice=option_price).impliedVolatility
        greeks = {
            'Delta': round(get_greeks.putDelta, 4),
            'Gamma': round(get_greeks.gamma, 4),
            'Rho': round(get_greeks.putRho, 4),
            'Vega': round(get_greeks.vega, 4),
            'Theta': round(get_greeks.putTheta, 4),
            'IV': round(impliedVolatility, 4)
        }

    else:
        impliedVolatility = mibian.BS([symbol_price, option_strike, r, exp_time], callPrice=option_price).impliedVolatility
        greeks = {
            'Delta': round(get_greeks.callDelta, 4),
            'Gamma': round(get_greeks.gamma, 4),
            'Rho': round(get_greeks.callRho, 4),
            'Vega': round(get_greeks.vega, 4),
            'Theta': round(get_greeks.callTheta, 4),
            'IV': round(impliedVolatility, 4)
        }

    return greeks