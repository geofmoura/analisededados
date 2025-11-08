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