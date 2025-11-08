import sqlite3
import time
from src.exchange import process_exchange_data
import os
from src.comexstat import process_comex_data
from src.utils import calculateTime, get_logger
from src.generate_report import generate_report_df
from src.query import QueryHandler
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

def analyze_market_share():
    """Análise de parcela de mercado por bloco econômico"""
    try:
        qh = QueryHandler('data/database.db')
        
        logger.info("Calculando parcela de mercado total...")
        market_share_total = qh.get_market_share_by_economic_block()
        
        if not market_share_total.empty:
            market_share_total.to_excel('data/market_share_analysis.xlsx', index=False)
            logger.debug(f"Análise de parcela de mercado salva com {len(market_share_total)} linhas")
            
            print("\n" + "="*80)
            print("RESUMO DA PARCELA DE MERCADO POR BLOCO ECONÔMICO")
            print("="*80)
            
            for ano in market_share_total['ano'].unique():
                dados_ano = market_share_total[market_share_total['ano'] == ano]
                print(f"\nANO: {ano}")
                print("-" * 60)
                
                for fluxo in dados_ano['fluxo'].unique():
                    dados_fluxo = dados_ano[dados_ano['fluxo'] == fluxo]
                    print(f"\n{fluxo}:")
                    print(f"{'Bloco Econômico':<25} {'Valor (USD)':<15} {'Parcela':<8}")
                    print("-" * 50)
                    
                    for _, row in dados_fluxo.head(5).iterrows():
                        print(f"{row['bloco_economico']:<25} ${row['valor_total']:>13,.0f} {row['parcela_mercado']:>7.2f}%")
        
        else:
            logger.warning("Nenhum dado encontrado para análise de parcela de mercado")
            
    except Exception as e:
        logger.error(f"Erro na análise de parcela de mercado: {e}")

analyze_market_share()
connection.close()

end_time = time.time()
logger.success(f"Algoritmo Finalizado com sucesso em {calculateTime(end_time, start_time)}")