from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

def get_players_positions(symbol):
    
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        print("Nenhuma posição aberta encontradacode={}".format(mt5.last_error()))
    else:
        for position in positions:
            print(f"Símbolo: {position.symbol}, Tipo: {'Compra' if position.type == 0 else 'Venda'}, Volume: {position.volume}")

def get_history_deals(symbol):

    from_date=datetime(2024,9,3)
    to_date=datetime.now()

    deals=mt5.history_deals_get(from_date, to_date, symbol=symbol)
    if deals==None:
        print("No deals, error code={}".format(mt5.last_error()))
    elif len(deals)> 0:
        print("history_deals_get({}, {},)={}".format(from_date,to_date,len(deals)))
    