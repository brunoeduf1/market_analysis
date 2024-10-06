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

    from_date=datetime(2023,9,13)
    to_date=datetime.now()

    deals=mt5.history_deals_total(from_date, to_date)
    if deals>0:
        print("Total deals=",deals)
    else:
        print("Deals not found in history")
    