import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from graphs.graph import analyze_trend, plot_graph
from stocks.setups import apply_setups
from stocks.get_indicators import get_iv_1y_rank, get_iv_1y_percentile, get_iv_current
from services.services import get_symbol_data
import pytz

symbols_list = [
    'ABEV3', 'ALPA4', 'ALOS3', 'ASAI3', 'AZUL4',
    'AZZA3', 'B3SA3', 'BPAC11', 'BBAS3', 'BBDC4',
    'BBSE3', 'BEEF3', 'BHIA3', 'BOVA11', 'BRAP4',
    'BRFS3', 'BRKM5', 'BRSR6', 'CCRO3', 'CMIG4',
    'CMIN3', 'COGN3', 'CPFE3', 'CPLE6', 'CSAN3',
    'CSNA3', 'CVCB3', 'CYRE3', 'DXCO3', 'ELET3',
    'ECOR3', 'EGIE3', 'EMBR3', 'ENEV3', 'EQTL3',
    'EZTC3', 'GGBR4', 'GOAU4', 'GOLL4', 'HAPV3',
    'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4',
    'JBSS3', 'JHSF3', 'KLBN11', 'LREN3', 'LWSA3',
    'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3',
    'PCAR3', 'PETR4', 'PETZ3', 'PRIO3', 'QUAL3',
    'RAIL3', 'RAIZ4', 'RADL3', 'RDOR3', 'RENT3',
    'BRAV3', 'SANB11', 'SBSP3', 'SLCE3', 'SMAL11',
    'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3',
    'UGPA3', 'USIM5', 'VBBR3', 'VALE3', 'VIVA3',
    'VIVT3', 'WEGE3', 'YDUQ3'
]

def get_candles(symbol, time_frame = 252):
    
    #timezone = pytz.timezone("America/Sao_Paulo")

    candles = mt5.copy_rates_range(
        symbol,
        mt5.TIMEFRAME_D1,
        datetime.today() - timedelta(days=time_frame), # Um ano e meio atrás
        datetime.today(),
    )

    df_candles = pd.DataFrame(candles)
    #df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s').dt.tz_localize('UTC').dt.tz_convert(timezone)
    df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s')

    return df_candles

def get_symbols_list():
    return symbols_list

def process_symbol(stocks, symbol):
    try:
        data = get_candles(symbol, 548)
        trend = analyze_trend(data)
        data = apply_setups(data)

        setups_ativos = []

        if data['setup_9_1_buy'].iloc[-1]:
            setups_ativos.append('9.1 de compra')
        if data['setup_9_1_sell'].iloc[-1]:
            setups_ativos.append('9.1 de venda')
        if data['setup_9_2_buy'].iloc[-1]:
            setups_ativos.append('9.2 de compra')
        if data['setup_9_2_sell'].iloc[-1]:
            setups_ativos.append('9.2 de venda')
        if data['setup_9_3_buy'].iloc[-1]:
            setups_ativos.append('9.3 de compra')
        if data['setup_9_3_sell'].iloc[-1]:
            setups_ativos.append('9.3 de venda')
        if data['setup_PC_buy'].iloc[-1]:
            setups_ativos.append('PC de compra')
        if data['setup_PC_sell'].iloc[-1]:
            setups_ativos.append('PC de venda')

        if setups_ativos:
            return {
                'symbol': symbol,
                'setups': setups_ativos,
                'iv_rank': get_iv_1y_rank(stocks, symbol),
                'iv_percentile': get_iv_1y_percentile(stocks, symbol),
                'iv_current': get_iv_current(stocks, symbol)
            }
            #plot_graph(symbol, data, trend)

    except Exception as e:
        print(f"Erro ao processar {symbol}: {e}")

def print_symbol_analisys(symbol):
    data = get_candles(symbol, 548)
    trend = analyze_trend(data)
    data = apply_setups(data)
    print(data[['setup_9_1_buy', 'setup_9_1_sell', 'setup_9_2_buy', 'setup_9_2_sell', 'setup_9_3_buy', 'setup_9_3_sell', 'setup_PC_buy', 'setup_PC_sell']])

def print_analisys_result():
    stocks, time = get_symbol_data()
    symbols = get_symbols_list()
    results = []

    for symbol in symbols:
        result = process_symbol(stocks, symbol)
        if result:
            results.append(result)

    file_name = 'robot_analysis.txt'

    with open(file_name, mode='w', encoding='utf-8') as file:

        results = sorted(results, key=lambda x: (x['iv_percentile'] is not None, x['iv_percentile']))
        print('Dados obtidos em: ' + str(convert_time_zone(time).strftime('%Y-%m-%d %H:%M:%S')))

        file.write('Dados de volatilidade atualizados em: ' + str(convert_time_zone(time).strftime('%d/%m/%Y às %H:%M:%S')) + '\n')
        file.write('Ativo - Setup armado - IV Percentil - IV Rank - Vol Implicita \n')
        for result in results:

            setups_str = ', '.join(result['setups'])

            print(
                f"{result['symbol']} - "
                f"{setups_str} - "
                f"IV Percentil: {result['iv_percentile']} - "
                f"IV Rank: {result['iv_rank']} - "
                f"Vol Implicita: {result['iv_current']}")  

            file.write(str(result['symbol']) + ' - ' +
                       str(setups_str) + ' - ' +
                       str(result['iv_percentile']) + ' - ' +
                       str(result['iv_rank']) + ' - ' + 
                       str(result['iv_current']) + '\n')

def plot_symbol_graph(symbol):
    data = get_candles(symbol)
    trend = analyze_trend(data)
    data = apply_setups(data)
    plot_graph(symbol, data, trend)

def convert_time_zone(time):
    utc = pytz.utc
    brasilia_time = pytz.timezone('America/Sao_Paulo')
    utc_time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_time = utc.localize(utc_time)
    brasilia_time = utc_time.astimezone(brasilia_time)

    return brasilia_time