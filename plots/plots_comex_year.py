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
    imports_df = imports_df.groupby(['ano'])['valor_fob_dolar'].sum().reset_index()
    
    paises = imports_df['ano'].tolist()
    valores = imports_df['valor_fob_dolar'].tolist()
    
    ax.plot(paises, valores,color='blue', marker='o')
    ax.set_title("Evolução do valor de Importação por ano (2017–2024)")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Valor FOB (US$)")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    
    for x, y in zip(paises, valores):
        ax.text(x, y + (2 * 1_000_000_000), format_usd_mi(y), ha='center', va='bottom',
            bbox=dict(
                facecolor='white',   
                alpha=0.6,           
                edgecolor='none',
                boxstyle='round,pad=0.3'
            )
        )

    

def exports_chart(df, ax):
    exports_df = df[df['fluxo'] == 'Exportação']
    exports_df = exports_df.groupby(['ano'])['valor_fob_dolar'].sum().reset_index()
    
    paises = exports_df['ano'].tolist()
    valores = exports_df['valor_fob_dolar'].tolist()
    
    bars2 = ax.plot(paises, valores, marker='o')
    ax.set_title("Evolução do valor de Exportação por ano (2017–2024)")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Valor FOB (US$)")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    
    for x, y in zip(paises, valores):
        ax.text(x, y + (2 * 1_000_000_000), format_usd_mi(y), ha='center', va='bottom',
            bbox=dict(
                facecolor='white',   
                alpha=0.6,           
                edgecolor='none',
                boxstyle='round,pad=0.3'
            )
        )



def plots_comex_year():
    connection = sqlite3.connect('data/database.db')
    df = get_comexstat_data(connection)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    imports_chart(df, ax1)
    exports_chart(df, ax2)

    plt.tight_layout()
    plt.show()
    
