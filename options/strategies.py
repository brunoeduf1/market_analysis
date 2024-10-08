from numpy import double
import pandas as pd
from options.options_info import  get_options_list


def tree_point_box(symbol, exp_call, exp_put):
    calls_df = get_options_list(symbol, exp_call)
    calls_df = pd.DataFrame(calls_df)
    
    puts_df = get_options_list(symbol, exp_put)
    puts_df = pd.DataFrame(puts_df)

    result = []
    for _, call1 in calls_df.iterrows():
        for _, call2 in calls_df.iterrows():
            if  call1['price'] > double(0.0) and call2['price'] > double(0.0) and call1['strike'] < call2['strike']:
                for _, put in puts_df.iterrows():
                    if put['price'] > double(0.0) and put['strike'] == call2['strike']:
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

def save_file_tree_point_box(symbol,results, filename="tree_point_box_results.txt"):
    with open(filename, "w") as file:
        file.write("Tree Point Box: " + symbol + "\n")
        file.write("Call Comprada - CC Preco - Call Vendida - CV Preco - Put Comprada - PC Preco - Custo Total - Lucro Garantido \n")
        for result in results:
            file.write(str(result['call_comprada']) + ' - ' + 
                       str(result['call_comprada_preco']) + ' - ' + 
                       str(result['call_vendida']) + ' - ' +
                       str(result['call_vendida_preco']) + ' - ' +  
                       str(result['put_comprada']) + ' - ' + 
                       str(result['put_comprada_preco']) + ' - ' +  
                       str(result['custo_total']) + ' - ' + 
                       str(result['lucro_garantido']) + '\n')