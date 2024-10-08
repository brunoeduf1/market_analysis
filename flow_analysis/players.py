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

    from_date=datetime(2024,10,7)
    to_date=datetime.now()

    deals = mt5.history_deals_get(from_date, to_date, symbol=symbol)

    if deals is None:
        print("Nenhum negócio encontrado para o ativo", symbol)
    else:
        total_deals = len(deals)
        print(f"Número total de negócios para {symbol}: {total_deals}")

def get_history_orders(symbol):
    from_date=datetime(2024,10,3)
    to_date=datetime.now()
    history_orders=mt5.history_orders_get(from_date, to_date, symbol=symbol)
    if history_orders is None:
        print("Total history orders=",symbol)
    else:
        print("Orders not found in history")

def get_orders(symbol):
    orders=mt5.orders_get(symbol=symbol)
    if orders is None:
        print("No orders, error code={}".format(mt5.last_error()))
    else:
        print("Total orders:",len(orders))
        # display all active orders
        for order in orders:
            print(order)
    print()
    