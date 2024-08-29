from options.options import get_expiration_time, get_options_info
from stocks.symbols_analysis import get_candles
import numpy as np
import math
from scipy.stats import norm

r = 0.105 # Taxa de juros livre de risco

def d1(S, K, T, sigma):
    return (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

def d2(S, K, T, sigma):
    return d1(S, K, T, sigma) - sigma * math.sqrt(T)

def call_option_price(symbol, option):
    S = get_symbol_price(symbol)
    K = get_options_info(option)['strike']
    T = get_expiration_time(option)
    sigma = calc_historic_vol(symbol)

    D1 = d1(S, K, T, sigma)
    D2 = d2(S, K, T, sigma)
    call_price = S * norm.cdf(D1) - K * math.exp(-r * T) * norm.cdf(D2)
    return call_price

def put_option_price(symbol, option):
    S = get_symbol_price(symbol)
    K = get_options_info(option)['strike']
    T = get_expiration_time(option)
    sigma = calc_historic_vol(symbol)

    D1 = d1(S, K, T, sigma)
    D2 = d2(S, K, T, sigma)
    put_price = K * math.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)
    return put_price

def calc_historic_vol(symbol, period=252):
    stocks = get_candles(symbol, 370)
    prices = stocks['close']
    returns = np.sum((prices - prices.shift(1)).dropna())
    volatility = np.sqrt((returns / (period)))
    return volatility

def get_symbol_price(symbol):
    stocks = get_candles(symbol)
    last_strike = stocks['close'].iloc[-1]
    return last_strike
    