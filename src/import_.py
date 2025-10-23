import pandas as pd

def process_import_data():

    df = pd.read_csv('data/import.csv', sep=';')
    
    grouped = df.groupby(['Ano', 'Mês'])['Valor US$ FOB'].mean().reset_index()
    grouped = grouped.rename(columns={
        'Valor US$ FOB': 'valor',
        'Ano': 'ano',
        'Mês': 'mes'
    })
    return grouped


if __name__ == "__main__":
    data = process_import_data()
    print(data)