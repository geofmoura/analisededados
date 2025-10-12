import pandas as pd

months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def process_exchange_data():
    df = pd.read_json('data/exchange.json')
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['mes'] = df['mes'].apply(lambda x: months[x - 1])
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    grouped = df.groupby(['ano', 'mes'])['valor'].mean().reset_index()
    
    return df   


if __name__ == "__main__":
    data = process_exchange_data()
    data.to_excel('data/excahnge.xlsx', index=False)
    print(data)