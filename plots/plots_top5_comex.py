import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from get_data.get_comexstat_data import get_comexstat_data

pd.set_option('display.max_columns', None)

def format_usd_mi(valor: float) -> str:
    valor_mi = valor / 1_000_000_000
    valor_formatado = f"{valor_mi:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {valor_formatado} Bi"

def imports_chart(df, ax):
    imports_df = df[df['fluxo'] == 'Importaçao']
    imports_df = imports_df.groupby(['pais'])['valor_fob_dolar'].sum().reset_index()
    imports_df = imports_df.sort_values(by='valor_fob_dolar', ascending=False).head(5)
    
    paises = imports_df['pais'].tolist()
    valores = imports_df['valor_fob_dolar'].tolist()
    
    bars1 = ax.bar(paises, valores)
    ax.set_title("Top 5 Importações")
    ax.set_xlabel("País")
    ax.set_ylabel("Valor FOB (US$)")
    ax.tick_params(axis='x', rotation=45)

    for bar in bars1:
        altura = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            altura,
            format_usd_mi(altura),
            ha="center", va="bottom"
        )

    

def exports_chart(df, ax):
    exports_df = df[df['fluxo'] == 'Exportação']
    exports_df = exports_df.groupby(['pais'])['valor_fob_dolar'].sum().reset_index()
    exports_df = exports_df.sort_values(by='valor_fob_dolar', ascending=False).head(5)
    
    paises = exports_df['pais'].tolist()
    valores = exports_df['valor_fob_dolar'].tolist()
    
    bars2 = ax.bar(paises, valores)
    ax.set_title("Top 5 Exportações")
    ax.set_xlabel("País")
    ax.set_ylabel("Valor FOB (US$)")
    ax.tick_params(axis='x', rotation=45)

    for bar in bars2:
        altura = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            altura,
            format_usd_mi(altura),
            ha="center", va="bottom"
        )

def top5_import_counties():
    connection = sqlite3.connect('data/database.db')
    df = get_comexstat_data(connection)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    imports_chart(df, ax1)
    exports_chart(df, ax2)

    plt.tight_layout()
    plt.show()
    
