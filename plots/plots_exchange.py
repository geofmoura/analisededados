import pandas as pd
import matplotlib.pyplot as plt

def carregar_dados():
    df = pd.read_excel('data/exchange.xlsx')
    print("Colunas no DataFrame:", df.columns.tolist())
    df = df.sort_values(by="data")
    df['data'] = pd.to_datetime(df['data'])
    return df

def grafico_media_anual(df):
    annual_avg = df.groupby(df['data'].dt.year)['valor'].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(annual_avg.index, annual_avg.values, color='blue', label='Média anual do câmbio', marker='o')
    plt.fill_between(annual_avg.index, annual_avg.values, color='skyblue', alpha=0.3)

    plt.title('Evolução da Média da Taxa de Câmbio no Tempo (2017–2024)')
    plt.xlabel('Ano')
    plt.ylabel('Taxa média (R$)')
    plt.legend()
    plt.grid(True)
    plt.xticks(annual_avg.index)
    plt.show()

def grafico_periodos_crises(df):

    if 'ano' not in df.columns:
        df['ano'] = df['data'].dt.year
    
    pre_covid = df[(df['ano'] >= 2017) & (df['ano'] <= 2019)].sort_values('data')
    covid = df[(df['ano'] >= 2020) & (df['ano'] <= 2021)].sort_values('data')
    ucrania = df[(df['ano'] >= 2022) & (df['ano'] <= 2023)].sort_values('data')

    pre_covid_mensal = pre_covid.groupby(pre_covid['data'].dt.to_period('M'))['valor'].mean()
    covid_mensal = covid.groupby(covid['data'].dt.to_period('M'))['valor'].mean()
    ucrania_mensal = ucrania.groupby(ucrania['data'].dt.to_period('M'))['valor'].mean()

    pre_covid_mensal.index = pre_covid_mensal.index.to_timestamp()
    covid_mensal.index = covid_mensal.index.to_timestamp()
    ucrania_mensal.index = ucrania_mensal.index.to_timestamp()

    plt.figure(figsize=(14, 8))
    width = 20

    plt.plot(pre_covid_mensal.index, pre_covid_mensal.values, label='Pré-Covid (2017-2019)', color='green', marker='o', linewidth=2)
    plt.plot(covid_mensal.index, covid_mensal.values, label='Covid (2020–2021)', color='orange', marker='o', linewidth=2)
    plt.plot(ucrania_mensal.index, ucrania_mensal.values, label='Guerra da Ucrânia (2022–2023)', color='red', marker='o', linewidth=2)

    plt.title('Variação Mensal da Taxa de Câmbio em Períodos de Crise')
    plt.xlabel('Mês')
    plt.ylabel('Taxa de média (R$)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    
def generate_exchange_plots():
    df = carregar_dados()
    print(f"Total de registros: {len(df)}")
    print(f"Período dos dados: {df['data'].min()} até {df['data'].max()}")
    
    grafico_media_anual(df)
    grafico_periodos_crises(df)

if __name__ == '__main__':
    generate_exchange_plots()