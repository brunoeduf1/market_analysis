import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from graph import analyze_trend, plot_graph
from setups import apply_setups, check_setups
from indicators import get_iv_1y_rank, get_iv_1y_percentile, get_iv_current

symbols_list = [
    'ABEV3', 'ALPA4', 'AMER3', 'ASAI3', 'AZUL4',
    'B3SA3', 'BAPC11', 'BBAS3', 'BBDC4', 'BBSE3',
    'BHIA3', 'BOVA11', 'BRAP4', 'BEEF3', 'BRFS3',
    'BRKM5', 'CIEL3', 'CMIG4', 'CPLE6', 'CSAN3',
    'CSNA3', 'CVCB3', 'CYRE3', 'DXCO3', 'ECOR3',
    'EGIE3', 'ELET3', 'EMBR3', 'ENEV3', 'EQTL3',
    'EZTC3', 'GGBR4', 'GOLL4', 'GOAU4', 'HAPV3',
    'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4',
    'JBSS3', 'JHSF3', 'KLBN11', 'LREN3', 'LWSA3',
    'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3',
    'PCAR3', 'PETR4', 'PETZ3', 'PRIO3', 'QUAL3',
    'RADL3', 'RAIL3', 'RAIZ4', 'RDOR3', 'RENT3',
    'RRRP3', 'SANB11', 'SBSP3', 'SLCE3', 'SOMA3',
    'SUZB3', 'TAEE11', 'TIMS3', 'UGPA3', 'USIM5',
    'VALE3', 'VBBR3', 'VIVT3', 'WEGE3'
]

def get_candles(symbol):

    # Obtém os dados das candles
    candles = mt5.copy_rates_range(
        symbol,
        mt5.TIMEFRAME_D1,
        datetime.today() - timedelta(days=548), # Um ano e meio atrás
        datetime.today(),
    )

    # Converte os dados para um DataFrame do Pandas
    df_candles = pd.DataFrame(candles)
    df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s')

    return df_candles

def get_symbols_list():
    return symbols_list

def process_symbol(stocks, symbol):
    try:
        data = get_candles(symbol)
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
