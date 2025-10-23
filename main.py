import plotly.graph_objects as go
import streamlit as st
from src.exchange import process_exchange_data, months
from src.import_ import process_import_data

st.title('Análise e Cambio / importações e importações')

df1 = process_exchange_data()
df2 = process_import_data()

grafico_df = df1[['mes', 'valor']].copy()
grafico_df = grafico_df.rename(columns={'valor': 'exchange_valor'})
grafico_df['import_valor'] = df2['valor'].values

grafico_df['mes_num'] = grafico_df['mes'].apply(lambda x: months.index(x) + 1)
grafico_df = grafico_df.sort_values('mes_num')

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=grafico_df['mes'],
    y=grafico_df['exchange_valor'],
    name='Câmbio',
    yaxis='y1',
))

fig.add_trace(go.Scatter(
    x=grafico_df['mes'],
    y=grafico_df['import_valor'],
    name='Importação',
    yaxis='y2'
))

fig.update_layout(
    yaxis=dict(title='Câmbio', showgrid=False),
    yaxis2=dict(title='Importação', overlaying='y', side='right', showgrid=False),
    xaxis=dict(title='Mês')
)

st.plotly_chart(fig)

