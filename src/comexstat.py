from logging import getLevelName
import basedosdados as bd
import time
from loguru import logger
import pandas as pd
from src.query import get_sql_query
from src.utils import calculateTime, get_logger

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
    logger.debug("Iniciando processamento dos dados do Comexstat")
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

    exports_top5 = (
        exports.groupby(['sigla_pais_iso3', 'sigla_pais_iso3_nome'], as_index=False)['valor_fob_dolar']
        .sum()
        .sort_values(by='valor_fob_dolar', ascending=False)
        .head(5)
    )

    imports_top5 = (
        imports.groupby(['sigla_pais_iso3', 'sigla_pais_iso3_nome'], as_index=False)['valor_fob_dolar']
        .sum()
        .sort_values(by='valor_fob_dolar', ascending=False)
        .head(5)
    )

    salvar_top5_excel(exports_top5, imports_top5)

    return ncm_isic, pais_bloco, exports, imports, exports_top5, imports_top5

if __name__ == "__main__":
    get_logger()
    process_comex_data()

def get_tpo5_paises(df, fluxo):
    logger.info(f"Calculando TOP 5 países em {fluxo.lower()}")
    top5 = (df.groupby('CO_PAIS')['VL_FOB']
            .sum()
            .sort_values(ascending=False)
            .head(5))
    
    return top5 