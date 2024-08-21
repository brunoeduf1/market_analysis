import requests
from bs4 import BeautifulSoup
import json

def get_symbol_data():
    try:
        url="https://opcoes.oplab.com.br/mercado-de-opcoes"

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        script_tag = soup.find('script', id='__NEXT_DATA__')
        if not script_tag:
            raise Exception("Script com dados JSON não encontrado")

        json_data = json.loads(script_tag.string)

        stocks = json_data['props']['pageProps']['stocks']
        time = json_data['props']['pageProps']['time']

        for stock in stocks:
            {
            'iv_1y_rank': stock.get('iv_1y_rank'),
            'iv_1y_percentile': stock.get('iv_1y_percentile'),
            'iv_current': stock.get('iv_current')
            }

        return stocks, time

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição: {e}")
    except ValueError as e:
        raise Exception(f"Erro ao processar a resposta JSON: {e}")