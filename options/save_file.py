def save_file_tree_point_box(symbol,results):
    filename="tree_point_box_results_" + symbol + "_.txt"
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
            
def save_file_box_spread(symbol,results):
    filename="box_spread_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Box Spread: " + symbol + "\n")
        file.write("Call Comprada - CC Preco - Put Comprada - PC Preco - Call Vendida - CV Preco - Put Vendida - PV Preco - Custo Total - Lucro Garantido \n")
        for result in results:
            file.write(str(result['call_comprada']) + ' - ' + 
                       str(result['call_comprada_preco']) + ' - ' + 
                       str(result['put_comprada']) + ' - ' + 
                       str(result['put_comprada_preco']) + ' - ' +  
                       str(result['call_vendida']) + ' - ' +
                       str(result['call_vendida_preco']) + ' - ' +  
                       str(result['put_vendida']) + ' - ' + 
                       str(result['put_vendida_preco']) + ' - ' + 
                       str(result['custo_total']) + ' - ' + 
                       str(result['lucro_garantido']) + '\n')
            
def save_file_conversion_reversal(symbol, results):
    filename = "conversion_reversal_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Conversion/Reversal: " + symbol + "\n")
        file.write("Call Vendida - CV Preco - Put Comprada - PC Preco - Custo Total - Lucro Garantido \n")
        for result in results:
            file.write(str(result['call_vendida']) + ' - ' +
                       str(result['call_vendida_preco']) + ' - ' +
                       str(result['put_comprada']) + ' - ' +
                       str(result['put_comprada_preco']) + ' - ' +
                       str(result['custo_total']) + ' - ' +
                       str(result['lucro_garantido']) + '\n')

def save_file_calendar_spread(symbol, results):
    filename = "calendar_spread_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Calendar Spread Arbitrage: " + symbol + "\n")
        file.write("Call Comprada - CC Preco - Call Vendida - CV Preco - Custo Total \n")
        for result in results:
            file.write(str(result['call_comprada']) + ' - ' +
                       str(result['call_comprada_preco']) + ' - ' +
                       str(result['call_vendida']) + ' - ' +
                       str(result['call_vendida_preco']) + ' - ' +
                       str(result['custo_total']) + '\n')

def save_file_butterfly_spread(symbol, results):
    filename = "butterfly_spread_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Butterfly Spread: " + symbol + "\n")
        file.write("Call Comprada Low - CCL Preco - Call Vendida Mid - CVM Preco - Call Comprada High - CCH Preco - Custo Total - Lucro Garantido \n")
        for result in results:
            file.write(str(result['call_comprada_low']) + ' - ' +
                       str(result['call_comprada_low_preco']) + ' - ' +
                       str(result['call_vendida_mid']) + ' - ' +
                       str(result['call_vendida_mid_preco']) + ' - ' +
                       str(result['call_comprada_high']) + ' - ' +
                       str(result['call_comprada_high_preco']) + ' - ' +
                       str(result['custo_total']) + ' - ' +
                       str(result['lucro_garantido']) + '\n')

def save_file_iron_condor(symbol, results):
    filename = "iron_condor_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Iron Condor: " + symbol + "\n")
        file.write("Call Comprada - CC Preco - Call Vendida - CV Preco - Put Comprada - PC Preco - Put Vendida - PV Preco - Custo Total - Lucro Garantido \n")
        for result in results:
            file.write(str(result['call_comprada']) + ' - ' +
                       str(result['call_comprada_preco']) + ' - ' +
                       str(result['call_vendida']) + ' - ' +
                       str(result['call_vendida_preco']) + ' - ' +
                       str(result['put_comprada']) + ' - ' +
                       str(result['put_comprada_preco']) + ' - ' +
                       str(result['put_vendida']) + ' - ' +
                       str(result['put_vendida_preco']) + ' - ' +
                       str(result['custo_total']) + ' - ' +
                       str(result['lucro_garantido']) + '\n')

def save_file_straddle_arbitrage(symbol, results):
    filename = "straddle_arbitrage_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Straddle Arbitrage: " + symbol + "\n")
        file.write("Call Comprada - CC Preco - Put Comprada - PC Preco - Custo Total \n")
        for result in results:
            file.write(str(result['call_comprada']) + ' - ' +
                       str(result['call_comprada_preco']) + ' - ' +
                       str(result['put_comprada']) + ' - ' +
                       str(result['put_comprada_preco']) + ' - ' +
                       str(result['custo_total']) + '\n')

def save_file_broken_wing_butterfly(symbol, results):
    filename = "broken_wing_butterfly_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Broken Wing Butterfly: " + symbol + "\n")
        file.write("Call Comprada Low - CCL Preco - Call Vendida Mid - CVM Preco - Call Comprada High - CCH Preco - Custo Total \n")
        for result in results:
            file.write(str(result['call_comprada_low']) + ' - ' +
                       str(result['call_comprada_low_preco']) + ' - ' +
                       str(result['call_vendida_mid']) + ' - ' +
                       str(result['call_vendida_mid_preco']) + ' - ' +
                       str(result['call_comprada_high']) + ' - ' +
                       str(result['call_comprada_high_preco']) + ' - ' +
                       str(result['custo_total']) + '\n')

def save_file_synthetic_arbitrage(symbol, results):
    filename = "synthetic_arbitrage_results_" + symbol + "_.txt"
    with open(filename, "w") as file:
        file.write("Synthetic Arbitrage: " + symbol + "\n")
        file.write("Call - Call Preco - Put - Put Preco - Custo Sintético - Lucro Arbitragem \n")
        for result in results:
            file.write(str(result['call']) + ' - ' +
                       str(result['call_preco']) + ' - ' +
                       str(result['put']) + ' - ' +
                       str(result['put_preco']) + ' - ' +
                       str(result['custo_sintetico']) + ' - ' +
                       str(result['lucro_arbitragem']) + '\n')