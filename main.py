import sys
import time
from src.comexstat import process_comex_data
from src.exchange import process_exchange_data
import os
from loguru import logger

start_time = time.time()
logger.remove()
logger.add(sys.stdout, level="DEBUG", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>", colorize=True, enqueue=True)
logger.info("Algoritimo Iniciado")

os.makedirs('data', exist_ok=True)
comex = process_comex_data()
exchange = process_exchange_data()

logger.debug(f"DataFrame 'comex' processado com {len(comex)} linhas e {len(comex.columns)} colunas.")
logger.debug(f"DataFrame 'exchange' processado com {len(exchange)} linhas e {len(exchange.columns)} colunas.")

logger.info("Salvando arquivo excel com os dados do ComexStat")
comex.to_excel('data/comexstat.xlsx', index=False, sheet_name='comexstat')

logger.info("Salvando arquivo excel com os dados de Câmbio")
exchange.to_excel('data/exchange.xlsx', index=False, sheet_name='excahnge')

end_time = time.time()
elapsed_time = end_time - start_time

logger.success(f"Algoritmo Finalizado com sucesso em {elapsed_time:.2f} segundos")


