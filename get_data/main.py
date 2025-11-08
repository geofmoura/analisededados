import sqlite3
import time
from exchange import process_exchange_data
import os
from comexstat import process_comex_data
from utils import calculateTime, get_logger
from generate_report import generate_report_df
logger = get_logger()

start_time = time.time()

logger.info("Algoritimo Iniciado")

os.makedirs('data', exist_ok=True)
ncm_isic, pais_bloco, exports, imports = process_comex_data()
exchange = process_exchange_data()

logger.debug(f"DataFrame 'ncm_isic' processado com {len(ncm_isic)} linhas.")
logger.debug(f"DataFrame 'pais_bloco' processado com {len(pais_bloco)} linhas.")
logger.debug(f"DataFrame 'exports' processado com {len(exports)} linhas.")
logger.debug(f"DataFrame 'imports' processado com {len(imports)} linhas.")
logger.debug(f"DataFrame 'exchange' processado com {len(exchange)} linhas")

logger.info("Salvando dados do ComexStat no banco sqlite")
connection = sqlite3.connect('data/database.db')

ncm_isic.to_sql('ncm_isic', connection, if_exists='replace', index=False)
pais_bloco.to_sql('pais_bloco', connection, if_exists='replace', index=False)
exports.to_sql('exports', connection, if_exists='replace', index=False)
imports.to_sql('imports', connection, if_exists='replace', index=False)

logger.info("Salvando arquivo excel com os dados agrupados de Comex")
report = generate_report_df(connection)
report.to_excel('data/comexstat.xlsx', index=False, sheet_name='comexstat')

logger.info("Salvando arquivo excel com os dados de Câmbio")
exchange.to_excel('data/exchange.xlsx', index=False, sheet_name='excahnge')

logger.info("Realizando análise de parcela de mercado por bloco econômico")

connection.close()

end_time = time.time()
logger.success(f"Algoritmo Finalizado com sucesso em {calculateTime(end_time, start_time)}")