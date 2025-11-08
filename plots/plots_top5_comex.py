import sqlite3
import pandas as pd

from get_data.get_comexstat_data import get_comexstat_data

pd.set_option('display.max_columns', None)

def top5_import_counties():
    connection = sqlite3.connect('data/database.db')
    df = get_comexstat_data(connection)
    
    
    print(df.head())
    
    return


if __name__ == "__main__":
    top5_import_counties()