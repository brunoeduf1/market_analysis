import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from keras.api.models import Sequential
from keras.api.layers import Dense, Dropout
import mplfinance as mpf

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
    data['target_volume'] = data['real_volume'].shift(-1)
    
    features = ['open', 'high', 'low', 'close', 'real_volume', 'spread']
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
    model.add(Dense(1024, input_dim=input_shape, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(512, input_dim=input_shape, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(5))  # 5 saídas: open, high, low, close, volume
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1, validation_split=0.2)
    return model
    
def evaluate_model(model, X_test, y_test):
    loss = model.evaluate(X_test, y_test, verbose=0)
    print(f"Loss: {loss}")

def predict_next_candles(model, X, scaler_X, scaler_y, num_candles=7):
    predictions = []
    last_candle = X[-1].reshape(1, -1)
    for _ in range(num_candles):
        next_candle_scaled = model.predict(last_candle)
        next_candle = scaler_y.inverse_transform(next_candle_scaled)
        predictions.append(next_candle.flatten())
        
        # Atualizar last_candle com a previsão atual para a próxima iteração
        last_candle = np.array([[
            next_candle[0][0], next_candle[0][1], next_candle[0][2], next_candle[0][3], next_candle[0][4], 0
        ]])
        last_candle = scaler_X.transform(last_candle)

    return predictions

def plot_candles(data, predictions, symbol):
    # Concatenar dados históricos com previsões
    future_dates = pd.date_range(start=data.index[-1], periods=len(predictions) + 1, freq='D')[1:]
    future_data = pd.DataFrame(predictions, columns=['open', 'high', 'low', 'close', 'real_volume'], index=future_dates)
    combined_data = pd.concat([data, future_data])
    # Preparar os dados para o mplfinance
    combined_data = combined_data[['open', 'high', 'low', 'close', 'real_volume']]
    combined_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    # Plotar o gráfico de candles
    mpf.plot(combined_data, type='candle', volume=True, style='charles', title=symbol, ylabel='Preço', ylabel_lower='Volume')

def run_machine_learning(symbol):

    timeframe = mt5.TIMEFRAME_D1
    num_candles = 110
    data = get_historical_data(symbol, timeframe, num_candles)
    X_train, X_test, y_train, y_test, scaler_X, scaler_y = prepare_data(data)
    model = build_model(X_train.shape[1])
    model = train_model(model, X_train, y_train)
    evaluate_model(model, X_test, y_test)

    next_candle_predictions = predict_next_candles(model, X_test, scaler_X, scaler_y, num_candles=7)
    print("Previsões dos próximos 7 candles:")
    for i, pred in enumerate(next_candle_predictions):
        print(f"Candle {i+1}: Abertura: {pred[0]}, Máxima: {pred[1]}, Mínima: {pred[2]}, Fechamento: {pred[3]}, Volume: {pred[4]}")

    plot_candles(data, next_candle_predictions, symbol)