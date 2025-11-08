import sqlite3
import pandas as pd

sql_query = """--sql
    SELECT
        dados.ano as ano,
        dados.mes as mes,
        dados.id_pais as id_pais,
        diretorio_id_ncm.id_isic_classe as id_isic_classe,
        dados.sigla_pais_iso3 AS sigla_pais_iso3,
        diretorio_sigla_pais_iso3.nome AS sigla_pais_iso3_nome,
        SUM(dados.valor_fob_dolar) as valor_fob_dolar
    FROM `{}` AS dados
    LEFT JOIN (
        SELECT DISTINCT id_ncm, id_isic_classe  FROM `basedosdados.br_bd_diretorios_mundo.nomenclatura_comum_mercosul`
    ) AS diretorio_id_ncm
    ON dados.id_ncm = diretorio_id_ncm.id_ncm
    
    LEFT JOIN (
        SELECT DISTINCT sigla_pais_iso3, nome  FROM `basedosdados.br_bd_diretorios_mundo.pais`
    ) AS diretorio_sigla_pais_iso3
    ON dados.sigla_pais_iso3 = diretorio_sigla_pais_iso3.sigla_pais_iso3
    
    WHERE
        --dados.ano >= 2017 and dados.ano <= 2024
        dados.ano = 2024 and dados.mes = 1
    GROUP BY 
        dados.ano,
        dados.mes,
        diretorio_id_ncm.id_isic_classe,
        dados.id_pais,
        diretorio_sigla_pais_iso3.nome,
        dados.sigla_pais_iso3
"""

def get_sql_query(table: str):
    if table == 'exports':
        return sql_query.format('basedosdados.br_me_comex_stat.ncm_exportacao')
    
    if table == 'imports':
        return sql_query.format('basedosdados.br_me_comex_stat.ncm_importacao')
    return ''


sql_query_market_share = """
    SELECT
        dados.ano as ano,
        dados.mes as mes,
        dados.fluxo as fluxo,
        blocos.bloco_economico as bloco_economico,
        SUM(dados.valor_fob_dolar) as valor_total,
        ROUND((SUM(dados.valor_fob_dolar) * 100.0 /
            SUM(SUM(dados.valor_fob_dolar)) OVER (PARTITION BY dados.ano, dados.mes, dados.fluxo)), 2) as parcela_mercado
FROM (
    -- Dados de Exportação
    SELECT
        ano,
        mes,
        'EXP' as fluxo,
        sigla_pais_iso3,
        valor_fob_dolar
    FROM 'basedosdados.br_me_comex_stat.ncm_exportacao'
    WHERE ano = 2024 AND mes = 1

    UNION ALL

    -- Dados de Importação
    SELECT
        ano,
        mes,
        'IMP' as fluxo,
        sigla_pais_iso3,
        valor_fob_dolar
    FROM 'basedosdados.br_me_comex_stat.ncm_importacao'
    WHERE ano = 2024 AND mes = 1
    ) AS dados
    LEFT JOIN 'PAIS_BLOCO' AS blocos
    ON dados.sigla_pais_iso3 = blocos.siglas_pais_iso3
    WHERE blocos.blocos_economico IS NOT NULL
    GROUP BY
        dados.ano,
        dados.mes,
        dados.fluxo,
        blocos.blocos_economico
    ORDER BY
        dados.ano,
        dados.mes,
        dados.fluxo,
        valor_total DESC
"""

class QueryHandler:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def execute_query(self, query, params=None):
        """Executa query no SQLite e retorna DataFrame"""
        try:
            conn = sqlite3.connect(self.db_path)
            if params:
                df = pd.read_read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro na consulta: {e}")
        return pd.DataFrame()

def get_market_share_by_economic_block(self, year=None, month=None, flow=None):
    """
    Calcula parcela de mercado por bloco econômico
    Args:
        year: Ano (ex: 2024)
        month: Mês (ex: 1)
        flow: 'EXP' ou 'IMP'
    Returns:
        DataFrame com: ano, fluxo, bloco_economico, valor_total, parcela_mercado
    """
    query = """
    SELECT
        strftime('%Y', date) as ano,
        flow as fluxo,
        pb.economic_block as bloco_economico,
        SUM(trade_usd) as valor_total,
        ROUND((SUM(trade_usd)) "100.0 /
            SUM(SUM(trade_usd)) OVER (PARTITION BY strftime('%Y', date), flow)), 2) as parcela_mercado
    FROM trade_data td
    JOIN PAIS_BLOCO pb ON td.country_code = pb.country_code
    WHERE 1=1
    """

    params = []
    if year:
        query += " AND strftime('%Y', date) = ?"
        params.append(str(year))
    if month:
        query += " AND strftime('%m', date) = ?"
        params.append(str(month).zfill(2))
    if flow:
        query += " AND flow = ?"
        params.append(flow)

    query += """
    GROUP BY ano, fluxo, bloco_economico
    ORDER BY ano, fluxo, valor_total DESC
    """

    return self.execute_query(query, params)

def get_market_share_direct(self):
    """Retorna a query SQL direta para usar na Base dos Dados"""
    return sql_query_market_share

def get_market_share_analysis(db_handler=None, year=None, month=None, flow=None):
    """
    Função principal para análise de parcela de mercado
    """
    if db_handler is None:
        db_handler = QueryHandler()

    return db_handler.get_market_share_by_economic_block(year, month, flow)

if __name__ == "__main__":
    qh = QueryHandler()

    print("=== Parcela de mercado Total ===")
    df_total = get_market_share_analysis(qh)
    print(df_total.head())

    print("\n=== Parcela de Mercado 2024 ===")
    df_2024 = get_market_share_analysis(qh, year=2024)
    print(df_2024.head())

    print("\n=== Exportações 2024 ===")
    df_exp_2024 = get_market_share_analysis(qh, year=2024, flow='EXP')
    print(df_exp_2024.head())

    print("\n=== Query para Bases de Dados ===")
    print(qh.get_market_share_direct())