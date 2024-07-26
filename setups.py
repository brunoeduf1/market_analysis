
def setup_9_1(data):

    data['EMA9_diff'] = data['EMA9'].diff()
    
    last_candle_index = len(data) - 1
    
    data['setup_9_1_buy'] = False
    data['setup_9_1_sell'] = False
    
    # Setup 9.1 de Compra
    if data['EMA9_diff'].iloc[last_candle_index - 1] < 0 and data['EMA9_diff'].iloc[last_candle_index] > 0:
        data['setup_9_1_buy'] = True
    
    # Setup 9.1 de Venda
    if data['EMA9_diff'].iloc[last_candle_index - 1] > 0 and data['EMA9_diff'].iloc[last_candle_index] < 0:
        data['setup_9_1_sell'] = True
    
    return data

def setup_9_2(data):
    data['setup_9_2_buy'] = False
    data['setup_9_2_sell'] = False
    
    last_candle_index = len(data) - 1
    
    # Setup 9.2 de Compra
    if data['EMA9'].iloc[last_candle_index] > data['EMA9'].iloc[last_candle_index - 1] and data['close'].iloc[last_candle_index] < data['low'].iloc[last_candle_index - 1]:
        data.at[last_candle_index, 'setup_9_2_buy'] = True
    
    # Setup 9.2 de Venda
    if data['EMA9'].iloc[last_candle_index] < data['EMA9'].iloc[last_candle_index - 1] and data['close'].iloc[last_candle_index] > data['high'].iloc[last_candle_index - 1]:
        data.at[last_candle_index, 'setup_9_2_sell'] = True
    
    return data

def setup_9_3(data):
    data['setup_9_3_buy'] = (data['high'].shift(1) < data['high']) & (data['close'] > data['high'].shift(1))
    data['setup_9_3_sell'] = (data['low'].shift(1) > data['low']) & (data['close'] < data['low'].shift(1))
    return data

def setup_PC(data):
    data['setup_PC_buy'] = (data['low'] <= data['SMA21']) & (data['high'] >= data['SMA21'])
    data['setup_PC_sell'] = (data['low'] <= data['SMA21']) & (data['high'] >= data['SMA21'])
    return data

def apply_setups(data):
    data = setup_9_1(data)
    data = setup_9_2(data)
    data = setup_9_3(data)
    data = setup_PC(data)
    return data

def check_setups(data):
    last_candle = data.iloc[-1]
    if last_candle['setup_9_1_buy']:
        return 'Setup 9.1 de compra ativado'
    if last_candle['setup_9_1_sell']:
        return 'Setup 9.1 de venda ativado'
    if last_candle['setup_9_2_buy']:
        return 'Setup 9.2 de compra ativado'
    if last_candle['setup_9_2_sell']:
        return 'Setup 9.2 de venda ativado'
    if last_candle['setup_9_3_buy']:
        return 'Setup 9.3 de compra ativado'
    if last_candle['setup_9_3_sell']:
        return 'Setup 9.3 de venda ativado'
    if last_candle['setup_PC_buy']:
        return 'Setup PC de compra ativado'
    if last_candle['setup_PC_sell']:
        return 'Setup PC de venda ativado'
    else:
        return 'Nenhum Setup detectado'
