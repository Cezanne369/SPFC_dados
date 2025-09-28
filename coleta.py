import requests
import pandas as pd
import os
from api import API_KEY

API = API_KEY
TEAM_ID = 126       
LEAGUE_ID = 71      
SEASON = 2023       
ARQUIVO = 'data/raw/spfc_jogos.csv'

def coleta_jogos():

    url = 'https://v3.football.api-sports.io/fixtures'
    
    headers = {
        'x-apisports-key': API_KEY
    }

    params = {
        'team': TEAM_ID,
        'league': LEAGUE_ID,
        'season': SEASON
    }

    print('Buscando dados na API...')

    response = requests.get(url, headers=headers, params=params)


    if response.status_code != 200:
        raise Exception(f'Erro na requisição: {response.status_code} - {response.text}')
    
    dados = response.json()


    if not dados['response']:
        print(" A API não retornou resultados para os parâmetros informados.")
        return 


    jogos = pd.json_normalize(dados['response'])

    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)


    jogos.to_csv(ARQUIVO, index=False, encoding='utf-8-sig')
    print(f'Dados salvos com sucesso em: {ARQUIVO}')

if __name__ == "__main__":
    coleta_jogos()
