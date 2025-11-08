from logging import getLevelName
import sqlite3
import basedosdados as bd
import time
from loguru import logger
import pandas as pd
from query import get_sql_query
from utils import calculateTime, get_logger

BINLLING_ID = 'taskplus-397900'

def get_ncm_isic_data():
    logger.debug("Carregando dados da tablea ncm_isic")
    isic = pd.read_excel('data/NCM_ISIC.xlsx')
    isic = isic[['CO_ISIC_CLASSE', 'NO_ISIC_SECAO']]
    isic['CO_ISIC_CLASSE'] = isic['CO_ISIC_CLASSE'].apply(lambda a: str(a).zfill(4))
    return isic

def get_pais_bloco_data():
    logger.debug("Carregando dados da tablea pais_bloco")
    bloco = pd.read_excel('data/PAIS_BLOCO.xlsx')
    bloco = bloco[['CO_PAIS', 'NO_BLOCO']]
    excluded_blocos = ['América do Sul', 'União Europeia - UE']
    bloco = bloco[bloco['NO_BLOCO'].isin(excluded_blocos)]
    return bloco

def get_exports_data():
    logger.debug("Baixando dados de exportação")
    start_time = time.time()
    df = bd.read_sql(query = get_sql_query('exports'), billing_project_id = BINLLING_ID)
    end_time = time.time()
    logger.debug(f"Finalizado download dos dados de exportação - time: {calculateTime(end_time, start_time)}")
    return df
    
def get_imports_data():
    logger.debug("Baixando dados de importação")
    start_time = time.time()
    df = bd.read_sql(query = get_sql_query('imports'), billing_project_id = BINLLING_ID)
    end_time = time.time()
    logger.debug(f"Finalizado download dos dados de importação - time: {calculateTime(end_time, start_time)}")
    return df

def process_comex_data():
    logger.info("Iniciando processamento dos dados do Comexstat")
    ncm_isic = get_ncm_isic_data()
    pais_bloco = get_pais_bloco_data()
    exports = get_exports_data()
    imports = get_imports_data()
    
    return (ncm_isic, pais_bloco, exports, imports)

if __name__ == "__main__":  
    get_logger()
    ncm_isic, pais_bloco, exports, imports = process_comex_data()
    
    connection = sqlite3.connect('data/database.db')

    ncm_isic.to_sql('ncm_isic', connection, if_exists='replace', index=False)
    pais_bloco.to_sql('pais_bloco', connection, if_exists='replace', index=False)
    exports.to_sql('exports', connection, if_exists='replace', index=False)
    imports.to_sql('imports', connection, if_exists='replace', index=False)

