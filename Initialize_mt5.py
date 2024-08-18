import MetaTrader5 as mt5

def initialize():
    # Inicializar o MetaTrader 5
    if not mt5.initialize():
        print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
        mt5.shutdown()
        exit()

    # Verificar se o login foi bem-sucedido
    account_info = mt5.account_info()
    if account_info is None:
        print(f"Falha ao fazer login no MetaTrader 5, código de erro: {mt5.last_error()}")
        mt5.shutdown()
        exit()
    else:
        print(f"Login bem-sucedido: {account_info}")