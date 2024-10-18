import MetaTrader5 as mt5

def initialize():

    if not mt5.initialize():
        print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
        mt5.shutdown()
        exit()

    account_info = mt5.account_info()
    if account_info is None:
        print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
        mt5.shutdown()
        exit()
    else:
        print(f"Login bem-sucedido: {account_info}")

    return "Inicialização bem-sucedida!"