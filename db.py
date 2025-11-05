import basedosdados as bd
import time
from loguru import logger
import sys
import sqlite3
import pandas as pd

logger.remove()
logger.add(sys.stdout, level="DEBUG", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>", colorize=True, enqueue=True)

billing_id = 'taskplus-397900'
query = """--sql
    SELECT
        dados.ano as ano,
        dados.mes as mes,
        dados.id_pais as id_pais,
        diretorio_id_ncm.id_isic_classe as id_isic_classe,
        dados.sigla_pais_iso3 AS sigla_pais_iso3,
        diretorio_sigla_pais_iso3.nome AS sigla_pais_iso3_nome,
        SUM(dados.valor_fob_dolar) as valor_fob_dolar
    FROM `basedosdados.br_me_comex_stat.ncm_exportacao` AS dados
    LEFT JOIN (
        SELECT DISTINCT id_ncm, id_isic_classe  FROM `basedosdados.br_bd_diretorios_mundo.nomenclatura_comum_mercosul`
    ) AS diretorio_id_ncm
    ON dados.id_ncm = diretorio_id_ncm.id_ncm
    
    LEFT JOIN (
        SELECT DISTINCT sigla_pais_iso3, nome  FROM `basedosdados.br_bd_diretorios_mundo.pais`
    ) AS diretorio_sigla_pais_iso3
    ON dados.sigla_pais_iso3 = diretorio_sigla_pais_iso3.sigla_pais_iso3
    
    WHERE 
        dados.ano >= 2017 and dados.ano <= 2024
        --dados.ano = 2024 and dados.mes = 1
    GROUP BY 
        dados.ano,
        dados.mes,
        diretorio_id_ncm.id_isic_classe,
        dados.id_pais,
        diretorio_sigla_pais_iso3.nome,
        dados.sigla_pais_iso3
"""

def calculateTime(end_time: int, start_time: int):
    elapsed_time = end_time - start_time
    if elapsed_time > 60:
        return f'{elapsed_time/60:.2f} min'
    return f'{elapsed_time:.2f} sec'

if __name__ == "__main__":
    
    connection = sqlite3.connect('database.sql')
    
    isic = pd.read_excel('data/NCM_ISIC.xlsx')
    isic = isic[['CO_ISIC_CLASSE', 'NO_ISIC_SECAO']]
    isic['CO_ISIC_CLASSE'] = isic['CO_ISIC_CLASSE'].apply(lambda a: str(a).zfill(4))
    
    print(isic.head())
    isic.to_sql('ncm_isic', connection, if_exists='replace', index=False)
    
    bloco = pd.read_excel('data/PAIS_BLOCO.xlsx')
    bloco = bloco[['CO_PAIS', 'NO_BLOCO']]
    
    excluded_blocos = ['América do Sul', 'União Europeia - UE']
    bloco = bloco[bloco['NO_BLOCO'].isin(excluded_blocos)]
    
    print(bloco.head())
    bloco.to_sql('pais_bloco', connection, if_exists='replace', index=False)
    
    start_time = time.time()
    logger.info("Algoritimo Iniciado")
    df = bd.read_sql(query = query, billing_project_id = billing_id)
    end_time = time.time()
    logger.success(f"Algoritmo Finalizado - {calculateTime(end_time, start_time)}")
    
    
    # df.to_sql('teste.csv', index=False)
    df.to_sql('comex', connection, if_exists='replace', index=False)
    print(df.head(200))
    print(df.shape)


