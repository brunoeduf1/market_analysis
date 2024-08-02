import requests
from bs4 import BeautifulSoup
import json

def get_symbol_data():
    try:
        url="https://opcoes.oplab.com.br/mercado-de-opcoes"

        # Fazendo a requisição GET
        response = requests.get(url)
        response.raise_for_status()  # Levanta uma exceção para códigos de status de erro

        # Analisando o HTML da resposta
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrando o script que contém os dados JSON
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if not script_tag:
            raise Exception("Script com dados JSON não encontrado")

        # Extraindo o conteúdo JSON do script
        json_data = json.loads(script_tag.string)

        # Extraindo os dados das ações
        stocks = json_data['props']['pageProps']['stocks']

        # Procurando o símbolo específico
        for stock in stocks:
            {
            'iv_1y_rank': stock.get('iv_1y_rank'),
            'iv_1y_percentile': stock.get('iv_1y_percentile'),
            'iv_current': stock.get('iv_current')
            }

        return stocks

    except requests.exceptions.RequestException as e:
        # Captura qualquer exceção relacionada à requisição
        raise Exception(f"Erro na requisição: {e}")
    except ValueError as e:
        # Captura exceções relacionadas à conversão de JSON
        raise Exception(f"Erro ao processar a resposta JSON: {e}")
