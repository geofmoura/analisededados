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
        SELECT DISTINCT id_ncm, id_isic_classe  
        FROM `basedosdados.br_bd_diretorios_mundo.nomenclatura_comum_mercosul`
    ) AS diretorio_id_ncm
    ON dados.id_ncm = diretorio_id_ncm.id_ncm
    
    LEFT JOIN (
        SELECT DISTINCT sigla_pais_iso3, nome  
        FROM `basedosdados.br_bd_diretorios_mundo.pais`
    ) AS diretorio_sigla_pais_iso3
    ON dados.sigla_pais_iso3 = diretorio_sigla_pais_iso3.sigla_pais_iso3
    
    WHERE
        dados.ano = 2024 AND dados.mes = 1
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
class QueryHandler:
    def __init__(self, db_path='data/database.db'):
        self.db_path = db_path

    def execute_query(self, query, params=None):
        """Executa query no SQLite e retorna DataFrame"""
        try:
            conn = sqlite3.connect(self.db_path)
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return pd.DataFrame()

    def get_market_share_by_economic_block(self, year=None, month=None, flow=None):
        """Calcula parcela de mercado por bloco econômico"""
        query = """
        SELECT
            strftime('%Y', date) as ano,
            flow as fluxo,
            pb.economic_block as bloco_economico,
            SUM(trade_usd) as valor_total,
            ROUND((SUM(trade_usd) * 100.0 /
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


def generate_report_df(connection, exports_top5, imports_top5):
    """Gera o relatório Excel com os dados do Comex"""
    try:
        # Lê os dados do banco
        exports_df = pd.read_sql("SELECT * FROM exports", connection)
        imports_df = pd.read_sql("SELECT * FROM imports", connection)
        
        # Cria o ExcelWriter
        with pd.ExcelWriter('data/relatorio_comex.xlsx', engine='openpyxl') as writer:
            # Aba com todos os dados
            exports_df.to_excel(writer, sheet_name='Comex_Dados', index=False)
            
            # Abas com TOP 5
            exports_top5.to_excel(writer, sheet_name='Top5_Exportacao', index=False)
            imports_top5.to_excel(writer, sheet_name='Top5_Importacao', index=False)
        
        print("Relatório Excel criado: data/relatorio_comex.xlsx")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return False