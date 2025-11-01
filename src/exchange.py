import requests
import json
import pandas as pd
import os

months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def fetch_exchange_data():
    base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    periods = [
            ("01/01/2010", "31/12/2014"),
            ("01/01/2015", "31/12/2024")
        ]

    all_data = []

    for start, end in periods:
        params = {
            "formato": "json",
            "dataInicial": start,
            "dataFinal": end
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            part_data = response.json()
            all_data.extend(part_data)
            print(f"Coletados {len(part_data)} registros de {start} a {end}.")
        else:
            print(f"Erro ao coletar dados de {start} a {end}: {response.status_code}")
            return None
    
    return all_data

def process_exchange_data(all_data):
    df = pd.DataFrame(all_data)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['mes'] = df['mes'].apply(lambda x: months[x - 1])
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    grouped = df.groupby(['ano', 'mes'])['valor'].mean().reset_index()
    
    return grouped   


if __name__ == "__main__":
    data_json = fetch_exchange_data()
    
    if data_json:
        data = process_exchange_data(data_json)
        os.makedirs('data', exist_ok=True)
        data.to_excel('data/exchange.xlsx', index=False)
        print("Arquivo 'exchange.xlsx' criado com sucesso.")
    else:
            print("A coleta falhou. Verifique a conexão ou o endereço da API.")