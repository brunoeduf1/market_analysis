# predictor.py

import MetaTrader5 as mt5
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from keras.api.models import Sequential
from keras.api.layers import Dense

def get_historical_data(symbol, timeframe, num_candles):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data

def prepare_data(data):
    data['target_open'] = data['open'].shift(-1)
    data['target_high'] = data['high'].shift(-1)
    data['target_low'] = data['low'].shift(-1)
    data['target_close'] = data['close'].shift(-1)
    data['target_volume'] = data['tick_volume'].shift(-1)

    features = ['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
    X = data[features]
    y = data[['target_open', 'target_high', 'target_low', 'target_close', 'target_volume']]

    # Remover NaN
    X = X.dropna()
    y = y.dropna()

    # Garantir que X e y tenham o mesmo número de amostras
    min_length = min(len(X), len(y))
    X = X.iloc[:min_length]
    y = y.iloc[:min_length]

    # Normalizar os dados
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, scaler_X, scaler_y

def build_model(input_shape):
    model = Sequential()
    model.add(Dense(64, input_dim=input_shape, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(5))  # 5 saídas: open, high, low, close, volume
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)
    return model

def evaluate_model(model, X_test, y_test):
    loss = model.evaluate(X_test, y_test, verbose=0)
    print(f"Loss: {loss}")

def predict_next_candle(model, X, scaler_X, scaler_y):
    last_candle = X[-1].reshape(1, -1)
    next_candle_scaled = model.predict(last_candle)
    next_candle = scaler_y.inverse_transform(next_candle_scaled)
    return next_candle.flatten()
