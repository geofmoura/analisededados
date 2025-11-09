import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from get_data.get_comexstat_data import get_comexstat_data

pd.set_option('display.max_columns', None)

def plots_pie_charts_by_class():
    connection = sqlite3.connect('data/database.db')
    df = get_comexstat_data(connection)

    df.columns = df.columns.str.lower()

    # Agora filtramos importação ou exportação normalmente
    df = df[df['fluxo'] == 'Exportação']  #Importaçao ou Exportação (exatamente como está escrito)

    # Filtra o período desejado
    df = df[(df['ano'] >= 2017) & (df['ano'] <= 2024)]

    # Agrupa por seção isic e soma o valor FOB
    resumo = (
        df.groupby('secao_isic')['valor_fob_dolar']
        .sum()
        .reset_index()
        .sort_values(by='valor_fob_dolar', ascending=False)
    )

    print(resumo)

    if resumo.empty:
        print("⚠ Não há dados de importação no período selecionado.")
        return

    # === GRÁFICO DE PIZZA ===
    plt.figure(figsize=(8, 6))
    plt.pie(resumo['valor_fob_dolar'], labels=resumo['secao_isic'], autopct='%1.1f%%')
    plt.title('Participação das exportações por Seção ISIC (2017–2024)')
    plt.tight_layout()
    plt.show()

    return resumo


if __name__ == "__main__":
    plots_pie_charts_by_class()