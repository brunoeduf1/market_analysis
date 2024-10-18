from numpy import double
import pandas as pd
from options.options_info import  get_options_list
from options.save_file import save_file_box_spread, save_file_broken_wing_butterfly, save_file_butterfly_spread, save_file_calendar_spread, save_file_conversion_reversal, save_file_iron_condor, save_file_straddle_arbitrage, save_file_synthetic_arbitrage, save_file_tree_point_box


def tree_point_box(symbol, exp_call, exp_put):
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)
    
    puts_df = get_options_list(symbol, exp_put)
    puts_df = pd.DataFrame(puts_df)

    result = []
    for _, call1 in calls_df.iterrows():
        for _, call2 in calls_df.iterrows():
            if  call1['price'] > double(0.2) and call2['price'] > double(0.2) and call1['strike'] < call2['strike']:
                for _, put in puts_df.iterrows():
                    if put['price'] > double(0.2) and put['strike'] == call2['strike']:
                        total_cost = call1['price'] - call2['price'] + put['ask']
                        if total_cost < (call2['strike'] - call1['strike']):
                            result.append({
                                "call_comprada": call1['name'],
                                "call_comprada_preco": call1['price'],
                                "call_vendida": call2['name'],
                                "call_vendida_preco": call2['price'],
                                "put_comprada": put['name'],
                                "put_comprada_preco": put['price'],
                                "custo_total": total_cost,
                                "lucro_garantido": (call2['strike'] - call1['strike']) - total_cost
                            })
    
    result_sorted = sorted(result, key=lambda x: x['lucro_garantido'], reverse=True)

    save_file_tree_point_box(symbol, result_sorted)
    
    return result_sorted



def box_spread(symbol, exp_call, exp_put):
    
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)
    
    puts_df = get_options_list(symbol, exp_put)
    puts_df = pd.DataFrame(puts_df)

    result = []

    for _, call_low in calls_df.iterrows():
        for _, call_high in calls_df.iterrows():
            if call_high['price'] > double(0.4) and call_low['price'] > double(0.4) and call_low['strike'] < call_high['strike']:
                for _, put_low in puts_df.iterrows():
                    for _, put_high in puts_df.iterrows():
                        if put_low['price'] > double(0.4) and put_high['price'] > double(0.4) and put_low['strike'] < put_high['strike']:
                            # Verifica se os strikes são compatíveis
                            if double(call_low['strike']) == double(put_low['strike']) and double(call_high['strike']) == double(put_high['strike']):
                                # Calcula o custo total
                                custo_total = double(call_low['price']) - double(call_high['price']) + double(put_high['price']) - double(put_low['price'])
                                lucro_garantido = (double(call_high['strike']) - double(call_low['strike'])) - double(custo_total)
                                if lucro_garantido > 0:
                                    result.append({
                                        "call_comprada": call_low['name'],
                                        "call_comprada_preco": call_low['price'],
                                        "put_comprada": put_high['name'],
                                        "put_comprada_preco": put_high['price'],
                                        "call_vendida": call_high['name'],
                                        "call_vendida_preco": call_high['price'],
                                        "put_vendida": put_low['name'],
                                        "put_vendida_preco": put_low['price'],
                                        "custo_total": custo_total,
                                        "lucro_garantido": lucro_garantido
                                    })

    
    result_sorted = sorted(result, key=lambda x: x['lucro_garantido'], reverse=True)
    save_file_box_spread(symbol, result_sorted)
    
    return result_sorted

def conversion_reversal(symbol, exp_call, exp_put):
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)
    
    puts_df = get_options_list(symbol, exp_put)
    puts_df = pd.DataFrame(puts_df)

    result = []

    for _, call in calls_df.iterrows():
        for _, put in puts_df.iterrows():
            if call['strike'] == put['strike']:
                # Calcula o custo total
                custo_total = call['price'] - put['price']
                lucro_garantido = call['strike'] - custo_total
                if lucro_garantido > 0:
                    result.append({
                        "call_vendida": call['name'],
                        "call_vendida_preco": call['price'],
                        "put_comprada": put['name'],
                        "put_comprada_preco": put['price'],
                        "custo_total": custo_total,
                        "lucro_garantido": lucro_garantido
                    })

    result_sorted = sorted(result, key=lambda x: x['lucro_garantido'], reverse=True)
    save_file_conversion_reversal(symbol, result_sorted)
    
    return result_sorted

def calendar_spread_arbitrage(symbol, exp_call1, exp_call2):
    calls_df1 = get_options_list(symbol, exp_call1)
    calls_df1 = pd.DataFrame(calls_df1)
    
    calls_df2 = get_options_list(symbol, exp_call2)
    calls_df2 = pd.DataFrame(calls_df2)

    result = []

    for _, call1 in calls_df1.iterrows():
        for _, call2 in calls_df2.iterrows():
            if call1['strike'] == call2['strike']:
                # Calcula o custo total
                custo_total = call1['price'] - call2['price']
                if custo_total < 0:
                    result.append({
                        "call_comprada": call1['name'],
                        "call_comprada_preco": call1['price'],
                        "call_vendida": call2['name'],
                        "call_vendida_preco": call2['price'],
                        "custo_total": custo_total
                    })

    result_sorted = sorted(result, key=lambda x: x['custo_total'])
    save_file_calendar_spread(symbol, result_sorted)
    
    return result_sorted

def butterfly_spread(symbol, exp_call):
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)

    result = []

    for _, call_low in calls_df.iterrows():
        for _, call_mid in calls_df.iterrows():
            for _, call_high in calls_df.iterrows():
                if call_low['strike'] < call_mid['strike'] < call_high['strike']:
                    # Calcula o custo total
                    custo_total = double(call_low['price']) - 2 * double(call_mid['price']) + double(call_high['price'])
                    lucro_garantido = (double(call_high['strike']) - double(call_mid['strike'])) - double(custo_total)
                    if lucro_garantido > 0:
                        result.append({
                            "call_comprada_low": call_low['name'],
                            "call_comprada_low_preco": call_low['price'],
                            "call_vendida_mid": call_mid['name'],
                            "call_vendida_mid_preco": call_mid['price'],
                            "call_comprada_high": call_high['name'],
                            "call_comprada_high_preco": call_high['price'],
                            "custo_total": custo_total,
                            "lucro_garantido": lucro_garantido
                        })

    result_sorted = sorted(result, key=lambda x: x['lucro_garantido'], reverse=True)
    save_file_butterfly_spread(symbol, result_sorted)
    
    return result_sorted

def iron_condor(symbol, exp_call, exp_put):
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)
    
    puts_df = get_options_list(symbol, exp_put)
    puts_df = pd.DataFrame(puts_df)

    result = []

    for _, call_low in calls_df.iterrows():
        for _, call_high in calls_df.iterrows():
            for _, put_low in puts_df.iterrows():
                for _, put_high in puts_df.iterrows():
                    if call_low['price'] > double(0.4) and call_high['price'] > double(0.4) and put_low['price'] > double(0.4) and put_high['price'] > double(0.4) and call_low['strike'] < call_high['strike'] and put_low['strike'] < put_high['strike']:
                        # Calcula o custo total
                        custo_total = double(call_low['price']) - double(call_high['price']) + double(put_high['price']) - double(put_low['price'])
                        lucro_garantido = double(call_high['strike']) - double(call_low['strike']) - double(custo_total)
                        if lucro_garantido > 0:
                            result.append({
                                "call_comprada": call_low['name'],
                                "call_comprada_preco": call_low['price'],
                                "call_vendida": call_high['name'],
                                "call_vendida_preco": call_high['price'],
                                "put_comprada": put_high['name'],
                                "put_comprada_preco": put_high['price'],
                                "put_vendida": put_low['name'],
                                "put_vendida_preco": put_low['price'],
                                "custo_total": custo_total,
                                "lucro_garantido": lucro_garantido
                            })

    result_sorted = sorted(result, key=lambda x: x['lucro_garantido'], reverse=True)
    save_file_iron_condor(symbol, result_sorted)
    
    return result_sorted

def straddle_arbitrage(symbol, exp_call, exp_put):
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)
    
    puts_df = get_options_list(symbol, exp_put)
    puts_df = pd.DataFrame(puts_df)

    result = []

    for _, call in calls_df.iterrows():
        for _, put in puts_df.iterrows():
            if call['strike'] == put['strike']:
                # Calcula o custo total
                custo_total = call['price'] + put['price']
                if custo_total < call['strike']:
                    result.append({
                        "call_comprada": call['name'],
                        "call_comprada_preco": call['price'],
                        "put_comprada": put['name'],
                        "put_comprada_preco": put['price'],
                        "custo_total": custo_total
                    })

    result_sorted = sorted(result, key=lambda x: x['custo_total'])
    save_file_straddle_arbitrage(symbol, result_sorted)
    
    return result_sorted

def broken_wing_butterfly(symbol, exp_call):
    # Supondo que get_options_list retorna uma lista de dicionários com preços numéricos
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)

    result = []

    for _, call_low in calls_df.iterrows():
        for _, call_mid in calls_df.iterrows():
            for _, call_high in calls_df.iterrows():
                # Verifica se os strikes são adequados para a Broken Wing Butterfly
                if call_low['price'] > double(0.4) and call_mid['price'] > double(0.4) and call_high['price'] > double(0.4) and call_low['strike'] < call_mid['strike'] < call_high['strike']:
                    # Certifique-se de que os preços são valores numéricos
                    preco_low = double(call_low['price'])
                    preco_mid = double(call_mid['price'])
                    preco_high = double(call_high['price'])

                    # Calcula o custo total
                    custo_total = preco_low - 2 * preco_mid + preco_high

                    # Verifica se o custo total é zero ou próximo de zero
                    if abs(custo_total) < 0.01:  # Considera custo zero ou muito próximo de zero
                        result.append({
                            "call_comprada_low": call_low['name'],
                            "call_comprada_low_preco": preco_low,
                            "call_vendida_mid": call_mid['name'],
                            "call_vendida_mid_preco": preco_mid,
                            "call_comprada_high": call_high['name'],
                            "call_comprada_high_preco": preco_high,
                            "custo_total": custo_total
                        })

    result_sorted = sorted(result, key=lambda x: x['custo_total'])
    save_file_broken_wing_butterfly(symbol, result_sorted)
    
    return result_sorted

def synthetic_arbitrage(symbol, exp_date):
    # Supondo que get_options_list retorna uma lista de dicionários com preços numéricos
    options_df = get_options_list(symbol, exp_date)
    options_df = pd.DataFrame(options_df)

    result = []

    for _, call in options_df.iterrows():
        for _, put in options_df.iterrows():
            # Verifica se os strikes e vencimentos são iguais
            if call['strike'] == put['strike'] and call['expiration'] == put['expiration']:
                # Certifique-se de que os preços são valores numéricos
                preco_call = float(call['price'])
                preco_put = float(put['price'])
                preco_ativo = float(call['underlying_price'])

                # Calcula o custo da posição sintética
                custo_sintetico = preco_call - preco_put

                # Calcula o lucro potencial da arbitragem
                lucro_arbitragem = preco_ativo - custo_sintetico

                if abs(lucro_arbitragem) > 0.01:  # Considera lucro significativo
                    result.append({
                        "call": call['name'],
                        "call_preco": preco_call,
                        "put": put['name'],
                        "put_preco": preco_put,
                        "custo_sintetico": custo_sintetico,
                        "lucro_arbitragem": lucro_arbitragem
                    })

    result_sorted = sorted(result, key=lambda x: x['lucro_arbitragem'], reverse=True)
    save_file_synthetic_arbitrage(symbol, result_sorted)
    
    return result_sorted