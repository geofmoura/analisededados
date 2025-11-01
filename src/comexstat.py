import pandas as pd 
import glob
import os
from loguru import logger

def process_comex_data():
    logger.info("Iniciando processamento dos dados do ComexStat")
    df = merge_csv_files()
    
    
    logger.debug(f"Agrupando dados")
    grouped = df.groupby(['Ano', 'Mês', 'Fluxo', 'Descrição ISIC Seção'])['Valor US$ FOB'].mean().reset_index()
    grouped = grouped.rename(columns={
        'Valor US$ FOB': 'valor',
        'Ano': 'ano',
        'Mês': 'mes'
    })
    
    grouped['mes'] = grouped['mes'].apply(lambda a : a.split('.')[0]) 
    
    grouped['data'] = pd.to_datetime(
        grouped['ano'].astype(str) + '/' + grouped['mes'].astype(str) + '/01',
        errors='coerce'
    )
    grouped = grouped.drop(['ano', 'mes'], axis=1)
    
    cols = ['data'] + [col for col in grouped.columns if col != 'data']
    grouped = grouped.reindex(columns=cols)
    
    logger.success(f"Finalizado processamento dos dados do ComexStat com {len(grouped)} linhas")
    return grouped


def merge_csv_files(directory='data'):
    # Lista todos os arquivos CSV da pasta especificada
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    dataframes = []
    for file in csv_files:
        logger.debug(f"Carregando arquivo: {os.path.basename(file)}")
        df = pd.read_csv(file, sep=';')
        dataframes.append(df)
    # Concatena todos os DataFrames em um único
    merged_df = pd.concat(dataframes, ignore_index=True)
    logger.debug(f"Carregado {len(merged_df)} linhas")
    return merged_df

if __name__ == "__main__":
    data = process_comex_data()
    data.to_excel('./data/report.xlsx', index=False, sheet_name='comexstat')
    print(data)