import MetaTrader5 as mt5
import pandas as pd

def get_players_positions(symbol):
    
    positions = mt5.positions_get(symbol)
    if positions is None:
        print("Nenhuma posição aberta encontrada")
    else:
        for position in positions:
            print(f"Símbolo: {position.symbol}, Tipo: {'Compra' if position.type == 0 else 'Venda'}, Volume: {position.volume}")
