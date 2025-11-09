import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

from get_data.get_comexstat_data import get_comexstat_data
from get_data.utils import format_usd_mi

pd.set_option("display.max_columns", None)

def imports_chat(df):
    # Agora filtramos importação ou exportação normalmente
    df = df[df["fluxo"] == "Importaçao"]  # Importaçao ou Exportação (exatamente como está escrito)

    # Agrupa por seção isic e soma o valor FOB
    resumo = (
        df.groupby("secao_isic")["valor_fob_dolar"]
        .sum()
        .reset_index()
        .sort_values(by="valor_fob_dolar", ascending=False)
    )

    print(resumo)

    for index, row in resumo.iterrows():
        print(format_usd_mi(row['valor_fob_dolar']))

    # === GRÁFICO DE PIZZA ===
    plt.figure(figsize=(8, 6))
    plt.pie(resumo["valor_fob_dolar"].to_list(), labels=resumo["secao_isic"].to_list(), autopct="%1.1f%%")
    plt.title("Participação das importações por Seção ISIC (2017–2024)")
    plt.tight_layout()

def exports_chat(df):
    # Agora filtramos importação ou exportação normalmente
    df = df[df["fluxo"] == "Exportação"]  # Importaçao ou Exportação (exatamente como está escrito)

    # Agrupa por seção isic e soma o valor FOB
    resumo = (
        df.groupby("secao_isic")["valor_fob_dolar"]
        .sum()
        .reset_index()
        .sort_values(by="valor_fob_dolar", ascending=False)
    )

    print(resumo)

    for index, row in resumo.iterrows():
        print(format_usd_mi(row['valor_fob_dolar']))

    # === GRÁFICO DE PIZZA ===
    plt.figure(figsize=(8, 6))
    plt.pie(resumo["valor_fob_dolar"].to_list(), labels=resumo["secao_isic"].to_list(), autopct="%1.1f%%")
    plt.title("Participação das exportações por Seção ISIC (2017–2024)")
    plt.tight_layout()

def plots_pie_charts_by_class():
    connection = sqlite3.connect("data/database.db")
    df = get_comexstat_data(connection)

    df.columns = df.columns.str.lower()
    imports_chat(df)
    exports_chat(df)

    plt.show()




if __name__ == "__main__":
    plots_pie_charts_by_class()
