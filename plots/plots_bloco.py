import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from get_data.get_comexstat_data import get_comexstat_data

pd.set_option('display.max_columns', None)

def carregar_dados_comercio():
    """
    Carrega osm dados de comércio exterior do arquivo Excel
    """
    connection = sqlite3.connect('data/database.db')
    df = get_comexstat_data(connection)

    return df
    

def processar_dados_mercado(df, fluxo='Importação'):
    """
    Processa os dados para calcular a parcela de mercado por bloco econômico
    """
    print(df.head(200))
    df = df[df['fluxo'] == fluxo]
    mercado_blocos = df.groupby('bloco_economico')['valor_fob_dolar'].sum().reset_index()
    total = mercado_blocos['valor_fob_dolar'].sum()
    mercado_blocos['percentual'] = (mercado_blocos['valor_fob_dolar'] / total) * 100
    mercado_blocos = mercado_blocos.sort_values('valor_fob_dolar', ascending=False)
        
    return mercado_blocos

def grafico_parcela_mercado_bloco(df, fluxo='Importação'):
    """
        Gera gráfico de barras da parcela de mercado por bloco econômico
    """
    dados = processar_dados_mercado(df, fluxo)

    plt.figure(figsize=(12, 8))

    bars = plt.bar(dados['bloco_economico'].tolist(), dados['percentual'].tolist(), color=plt.cm.Set3(range(len(dados))))
    for bar, valor in zip(bars, dados['percentual']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{valor:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.title(f'Parcela do Mercado por Bloco Econômico - {fluxo}')
    plt.xlabel('Bloco Econômico')
    plt.ylabel('Participação no Mercado (%)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    return plt


def analise_evolucao_temporal(df,  fluxo='Importação'):
    """
    Analisa a evolução temporal da participação dos blocos econômicos
    """

    anos = sorted(df['ano'].unique())

    fig, axes = plt.subplots(2,2, figsize=(15, 12))
    axes = axes.flatten()

    for i, ano in enumerate(anos[-4:]):
        dados = processar_dados_mercado(df, ano, fluxo)

        axes[i].pie(dados['percentual'], labels=dados['bloco_economico'], autopct='%1.1f%%', startangle=90)
        axes[i].set_title(f'Distribuição por Bloco - {fluxo} {ano}')

    plt.tight_layout()
    return plt


def generate_bloco_economico_plots():
    """
    Função principal para gerar todos os gráficos de bloco econômico
    """
    df = carregar_dados_comercio()

    print(f"Total de registros de comércio: {len(df)}")
    print(f"Anos disponíveis: {sorted(df['ano'].unique())}")
    print(f"Fluxos disponíveis: {df['fluxo'].unique()}")

    plt1 = grafico_parcela_mercado_bloco(df, 'Importaçao')
    plt1.show()

    plt2 = grafico_parcela_mercado_bloco(df, 'Exportação')
    plt2.show()

    # plt3 = analise_evolucao_temporal(df, 'Importação')
    # plt3.show()

if __name__ == '__main__':
    generate_bloco_economico_plots()