import sys
from loguru import logger
import requests
import json
import pandas as pd
import os

months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def fetch_exchange_data():
    logger.debug("Iniciado coleta de dados da api")
    
    base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    periods = [
            ("01/01/2017", "31/12/2018"),
            ("01/01/2019", "31/12/2020"),
            ("01/01/2021", "31/12/2022"),
            ("01/01/2023", "31/12/2024"),
        ]

    all_data = []

    for start, end in periods:
        logger.debug(f"Obtendo dados do peíodo de {start} a {end}")
        params = {
            "formato": "json",
            "dataInicial": start,
            "dataFinal": end
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            part_data = response.json()
            all_data.extend(part_data)
            logger.debug(f"Coletados {len(part_data)}")
        else:
            msg = response.text.strip() or response.reason or f"status {response.status_code}"
            raise RuntimeError(f"Requisição retornou status {response.status_code} para {start} a {end}: {msg}")
        
    logger.debug(f"Finalizado coleta de dados da api, carregado {len(all_data)} linhas")
    return all_data

def process_exchange_data():
    logger.info("Iniciando processamento dos dados de Câmbio")
    
    try:
        data_json = fetch_exchange_data()
    except Exception as e:
        logger.error(f"A coleta falhou: {e}")
        sys.exit(1)
    
    logger.debug("Tratanto os dados da API com o Pandas")
    df = pd.DataFrame(data_json)
    
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['mes'] = df['mes'].apply(lambda x: months[x - 1])
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    grouped = df.groupby(['ano', 'mes'])['valor'].mean().reset_index()
    
    grouped['mes'] = grouped['mes'].apply(lambda a : months.index(a) + 1) 
    
    grouped['data'] = pd.to_datetime(
        grouped['ano'].astype(str) + '/' + grouped['mes'].astype(str) + '/01',
        errors='coerce'
    )
    grouped = grouped.drop(['ano', 'mes'], axis=1)
    
    logger.success("Finalizado processamento dos dados de Câmbio")
    return grouped


if __name__ == "__main__":
    df= process_exchange_data()
    df.to_excel('data/exchange.xlsx', index=False)
    print("Arquivo 'exchange.xlsx' criado com sucesso.")
    
