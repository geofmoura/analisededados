import sqlite3
import pandas as pd

def generate__df(db_conn, exports_top5, imports_top5, caminho_arquivo='data/relatorio_comex.xlsx'):
    """
    Gera um relatório Excel consolidado com todas as tabelas:
    - Exportações completas
    - Importações completas
    - Top 5 Exportações
    - Top 5 Importações
    """

    query = """--sql
        SELECT 
            ano,
            mes,
            sigla_pais_iso3 as sigla_pais,
            sigla_pais_iso3_nome as pais,
            ncm_isic.NO_ISIC_SECAO as secao_isic,
            pais_bloco.NO_BLOCO as bloco_economico,
            valor_fob_dolar
        FROM {} 
        LEFT JOIN ncm_isic ON ncm_isic.CO_ISIC_CLASSE = id_isic_classe
        LEFT JOIN pais_bloco ON id_pais = pais_bloco.CO_PAIS                  
    """

    exports = pd.read_sql_query(query.format('exports'), con=db_conn)
    exports['fluxo'] = 'Exportação'

    imports = pd.read_sql_query(query.format('imports'), con=db_conn)
    imports['fluxo'] = 'Importação'

    df = pd.concat([exports, imports])

    with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Comex_Dados', index=False)
        exports_top5.to_excel(writer, sheet_name='Top5_Exportacao', index=False)
        imports_top5.to_excel(writer, sheet_name='Top5_Importacao', index=False)

    print(f"Relatório salvo em: {caminho_arquivo}")

    return df


if __name__ == '__main__':
    connection = sqlite3.connect('data/database.db')

    exports_top5 = pd.DataFrame()
    imports_top5 = pd.DataFrame()

    generate_report_df(connection, exports_top5, imports_top5)
