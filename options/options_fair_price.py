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
    stocks = get_candles(symbol, 30)
    prices = stocks['close']
    returns = np.log(prices / prices.shift(1)).round(4)
    volatility = (returns.std() * np.sqrt(252)).round(4)

    return volatility

def calc_exponential_historic_vol(symbol):
    df = get_candles(symbol,365)
    df['Return'] = df['close'].pct_change()
    lambda_ = 1 / (22 +1)
    df['EWMA Volatility'] = df['Return'].ewm(alpha=lambda_, adjust=False).std()
    df['Annualized EWMA Volatility'] = df['EWMA Volatility'] * np.sqrt(252)
    print(df[['close', 'Annualized EWMA Volatility']].tail())

def calc_exponential_historic_vol2(symbol):
    df = get_candles(symbol,30)
    df['Parkinson Volatility'] = (1 / (4 * np.log(2))) * ((np.log(df['high'] / df['low'])) ** 2)
    parkinson_volatility = np.sqrt(df['Parkinson Volatility'].mean())
    annualized_parkinson_volatility = parkinson_volatility * np.sqrt(252/22)
    print(f"Volatilidade Anualizada de Parkinson (22 dias): {annualized_parkinson_volatility:.2%}")

def calc_exponential_historic_vol3(symbol):
    df = get_candles(symbol,365)
    df['Parkinson Volatility'] = (1 / (4 * np.log(2))) * ((np.log(df['high'] / df['low'])) ** 2)
    df['EMA Volatility'] = df['Parkinson Volatility'].ewm(span=22, adjust=False).mean()
    parkinson_volatility = np.sqrt(df['EMA Volatility'].iloc[-1])
    annualized_parkinson_volatility = parkinson_volatility * np.sqrt(252)
    print(f"Volatilidade Anualizada de Parkinson (EMA 22 dias): {annualized_parkinson_volatility:.2%}")

def calc_exponential_historic_vol4(symbol):
    df = get_candles(symbol,30)
    df['Return'] = df['close'].pct_change()
    N = 22
    lambda_ = 1 - (2 / (N + 1))
    initial_return = df['Return'].dropna().iloc[0]
    df['EWMA Volatility'] = 0.0
    df['EWMA Volatility'].iloc[1] = initial_return ** 2
    for t in range(2, len(df)):
        df['EWMA Volatility'].iloc[t] = (lambda_ * df['EWMA Volatility'].iloc[t-1] + (1 - lambda_) * df['Return'].iloc[t] ** 2)
    df['Annualized EWMA Volatility'] = np.sqrt(df['EWMA Volatility'] * 252/N)
    current_volatility = df['Annualized EWMA Volatility'].iloc[-1]
    print(f"Volatilidade Anualizada EWMA (22 dias): {current_volatility:.2%}")

def calc_exponential_historic_vol5(symbol):
    df = get_candles(symbol,30)
    df['previous_close'] = df['close'].shift(1)
    df['high_low'] = df['high'] - df['low']
    df['high_previous_close'] = abs(df['high'] - df['previous_close'])
    df['low_previous_close'] = abs(df['low'] - df['previous_close'])
    df['tr'] = df[['high_low', 'high_previous_close', 'low_previous_close']].max(axis=1)
    df['atr'] = df['tr'].ewm(span=21, adjust=False).mean()
    volatility = df['atr'].iloc[-1]

    return volatility

    

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
    