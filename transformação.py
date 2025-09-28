import pandas as pd
import os

input_file = 'data/raw/spfc_jogos.csv' 
output_file = 'data/processed/spfc_jogos_tratados.csv'

def transformar_dados():
    print(f'Lendo os dados brutos: {input_file}')

    if not os.path.exists(input_file):
        raise FileNotFoundError(f'Arquivo não encontrado: {input_file}. Execute o script "coleta.py" primeiro.')
    
    df = pd.read_csv(input_file)

    print('Iniciando a transformação dos dados...')

    colunas_selecionadas = {
        'fixture.id': 'id_partida',
        'fixture.date': 'data_partida',
        'league.name': 'campeonato',
        'league.round': 'rodada',
        'teams.home.name': 'time_casa',
        'teams.away.name': 'time_fora',
        'goals.home': 'gols_casa',
        'goals.away': 'gols_fora',
        'score.fulltime.home': 'placar_final_casa',
        'score.fulltime.away': 'placar_final_fora'
    }

    df_tratado = df[list(colunas_selecionadas.keys())].copy()

    df_tratado.rename(columns=colunas_selecionadas, inplace=True)

    df_tratado['data_partida'] = pd.to_datetime (df_tratado['data_partida']).dt.strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    df_tratado.to_csv(output_file, index=False, encoding= 'utf-8-sig')

    print(f'Dados transformados e salvos em: {output_file}')
    print('\n Amostra dos dados tratados: ')
    print(df_tratado.head())

if __name__ == "__main__":
    transformar_dados()