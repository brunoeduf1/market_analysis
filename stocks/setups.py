# Setups 9.1, 9.2, 9.3 e PC de Larry Williams

def setup_9_1(data):

    data['time'] = data.index
    data = data.reset_index(drop=True)

    data['EMA9_diff'] = data['EMA9'].diff()
    
    
    data['setup_9_1_buy'] = False
    data['setup_9_1_sell'] = False
    
    # Setup 9.1 Buy
    data['setup_9_1_buy'] = (
        (data['EMA9_diff'].shift(1) < 0) & 
        (data['EMA9_diff'] > 0)
    )
    
    # Setup 9.1 Sell
    data['setup_9_1_sell'] = (
        (data['EMA9_diff'].shift(1) > 0) & 
        (data['EMA9_diff'] < 0)
    )
    
    data = data.set_index('time')

    return data

def setup_9_2(data):
    data['time'] = data.index
    data = data.reset_index(drop=True)
    
    data['setup_9_2_buy'] = False
    data['setup_9_2_sell'] = False
    
    # Setup 9.2 Buy
    data['setup_9_2_buy'] = (
        (data['EMA9'] > data['EMA9'].shift(1)) & 
        (data['close'].shift(1) < data['open'].shift(1)) & 
        (data['close'] < data['low'].shift(1))
    )
    
    # Setup 9.2 de Sell
    data['setup_9_2_sell'] = (
        (data['EMA9'] < data['EMA9'].shift(1)) & 
        (data['close'].shift(1) > data['open'].shift(1)) & 
        (data['close'] > data['high'].shift(1))
    )

    data = data.set_index('time')
    
    return data

def setup_9_3(data):

    data['time'] = data.index
    data = data.reset_index(drop=True)

    data['EMA9_diff'] = data['EMA9'].diff()
    
    data['setup_9_3_buy'] = False
    data['setup_9_3_sell'] = False
    
    # Setup 9.3 de Buy
    data['setup_9_3_buy'] = (
        (data['EMA9'] > data['EMA9'].shift(1)) &
        (
            ((data['close'].shift(2) > data['open'].shift(2)) &  # Candle de alta [-2]
             (data['close'].shift(1) < data['open'].shift(1)) &  # Candle de baixa [-1]
             (data['open'].shift(1) <= data['close'].shift(2)) &
             (data['close'].shift(1) >= data['open'].shift(2)) &
             (
                 ((data['close'] < data['open']) &  # Candle de baixa [0]
                  (data['open'] <= data['close'].shift(2)) &
                  (data['close'] >= data['open'].shift(2))) |
                 ((data['close'] > data['open']) &  # Candle de alta [0]
                  (data['close'] <= data['close'].shift(2)) &
                  (data['open'] >= data['open'].shift(2)))
             )) |
            ((data['close'].shift(2) > data['open'].shift(2)) &  # Candle de alta [-2]
             (data['close'].shift(1) > data['open'].shift(1)) &  # Candle de alta [-1]
             (data['close'].shift(1) <= data['close'].shift(2)) &
             (data['open'].shift(1) >= data['open'].shift(2)) &
             (
                 ((data['close'] > data['open']) &  # Candle de alta [0]
                  (data['close'] <= data['close'].shift(2)) &
                  (data['open'] >= data['open'].shift(2))) |
                 ((data['close'] < data['open']) &  # Candle de baixa [0]
                  (data['open'] <= data['close'].shift(2)) &
                  (data['close'] >= data['open'].shift(2)))
             ))
        )
    )
    
    # Setup 9.3 de Sell
    data['setup_9_3_sell'] = (
        (data['EMA9'] < data['EMA9'].shift(1)) &
        (
            ((data['close'].shift(2) < data['open'].shift(2)) &  # Candle de baixa [-2]
             (data['close'].shift(1) < data['open'].shift(1)) &  # Candle de baixa [-1]
             (data['open'].shift(1) <= data['open'].shift(2)) &
             (data['close'].shift(1) >= data['close'].shift(2)) &
             (
                 ((data['close'] < data['open']) &  # Candle de baixa [0]
                  (data['open'] <= data['open'].shift(2)) &
                  (data['close'] >= data['close'].shift(2))) |
                 ((data['close'] > data['open']) &  # Candle de alta [0]
                  (data['close'] <= data['open'].shift(2)) &
                  (data['open'] >= data['close'].shift(2)))
             )) |
            ((data['close'].shift(2) < data['open'].shift(2)) &  # Candle de baixa [-2]
             (data['close'].shift(1) > data['open'].shift(1)) &  # Candle de alta [-1]
             (data['close'].shift(1) <= data['open'].shift(2)) &
             (data['open'].shift(1) >= data['close'].shift(2)) &
             (
                 ((data['close'] > data['open']) &  # Candle de alta [0]
                  (data['close'] <= data['open'].shift(2)) &
                  (data['open'] >= data['close'].shift(2))) |
                 ((data['close'] < data['open']) &  # Candle de baixa [0]
                  (data['open'] <= data['open'].shift(2)) &
                  (data['close'] >= data['close'].shift(2)))
             ))
        )
    )

    data = data.set_index('time')
    
    return data

def setup_PC(data):
    data['time'] = data.index
    data = data.reset_index(drop=True)
    
    data['setup_PC_buy'] = False
    data['setup_PC_sell'] = False

    # Setup PC de Buy
    data['setup_PC_buy'] = (
        (data['SMA21'] > data['SMA21'].shift(1)) &
        (data['low'].shift(1) > data['SMA21'].shift(1)) &
        (data['low'] <= data['SMA21']) &
        (data['high'] >= data['SMA21'])
    )
    
    # Setup PC de Sell
    data['setup_PC_sell'] = (
        (data['SMA21'] < data['SMA21'].shift(1)) &
        (data['high'].shift(1) < data['SMA21'].shift(1)) &
        (data['low'] <= data['SMA21']) &
        (data['high'] >= data['SMA21'])
    )

    data = data.set_index('time')

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
        return 'Setup 9.1 de compra'
    if last_candle['setup_9_1_sell']:
        return 'Setup 9.1 de venda'
    if last_candle['setup_9_2_buy']:
        return 'Setup 9.2 de compra'
    if last_candle['setup_9_2_sell']:
        return 'Setup 9.2 de venda'
    if last_candle['setup_9_3_buy']:
        return 'Setup 9.3 de compra'
    if last_candle['setup_9_3_sell']:
        return 'Setup 9.3 de venda'
    if last_candle['setup_PC_buy']:
        return 'Setup PC de compra'
    if last_candle['setup_PC_sell']:
        return 'Setup PC de venda'
    else:
        return 'Nenhum Setup detectado'
