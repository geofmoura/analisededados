import sqlite3
import pandas as pd

def get_comexstat_data(db_conn):

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
    imports['fluxo'] = 'Importaçao'

    df = pd.concat([exports, imports])
    df = df[df['bloco_economico'] != None]
    
    # df['bloco_economico'] = df['bloco_economico'].apply(lambda item: 'Outros' if item is None else item)
    
    return df

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    connection = sqlite3.connect('data/database.db')
    df = get_comexstat_data(connection)
    
    print(df.head(200))