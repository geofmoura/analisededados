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
        return False

    os.makedirs('data', exist_ok=True)

    with open('data/exchange.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("Dados combinados e salvos em 'data/exchange.json'.")
    return True

def process_exchange_data():
    df = pd.read_json('data/exchange.json', encoding='utf-8')
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['mes'] = df['mes'].apply(lambda x: months[x - 1])
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    grouped = df.groupby(['ano', 'mes'])['valor'].mean().reset_index()
    
    return grouped   


if __name__ == "__main__":
    success = fetch_exchange_data()
    
    if success and os.path.exists('data/exchange.json'):
        data = process_exchange_data()
        data.to_excel('data/exchange.xlsx', index=False)
        print("Arquivo 'exchange.xlsx' criado com sucesso.")
    else:
        print("A coleta falhou. Verifique a conexão ou o enereço da API.")