from options.options_info import get_expiration_time, get_options_info, identify_option_type
from stocks.symbols_analysis import get_candles
import numpy as np
import math
from scipy.stats import norm

r = 0.104 # Taxa de juros livre de risco

def d1(S, K, T, sigma):
    return (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

def d2(S, K, T, sigma):
    return d1(S, K, T, sigma) - sigma * math.sqrt(T)

def calc_historic_vol(symbol):
    stocks = get_candles(symbol, 365)
    prices = stocks['close']
    returns = np.log(prices / prices.shift(1)).round(4)
    volatility = (returns.std() * np.sqrt(252)).round(4)

    return volatility

def calc_exponential_historic_vol(symbol):
    stocks = get_candles(symbol,365)
    prices = stocks['close']
    returns = np.log(prices / prices.shift(1)).round(4)
    span = 22
    squared_returns = returns ** 2
    exp_volatility = np.sqrt(squared_returns.ewm(span=span, adjust=False).mean() * 252).round(4)

    return exp_volatility.iloc[-1]

def get_option_fair_price(symbol, option):
    S = get_symbol_price(symbol)
    K = get_options_info(option)['strike']
    T = get_expiration_time(option)
    sigma = calc_historic_vol(symbol)

    D1 = d1(S, K, T, sigma)
    D2 = d2(S, K, T, sigma)

    option_type = identify_option_type(option)

    if(option_type == 'put'):
        price = K * math.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)
    else:
        price = S * norm.cdf(D1) - K * math.exp(-r * T) * norm.cdf(D2)

    return round(price,2)

def get_symbol_price(symbol):
    stocks = get_candles(symbol)
    last_strike = stocks['close'].iloc[-1]
    return last_strike

def get_interest_rate():
    return r
    