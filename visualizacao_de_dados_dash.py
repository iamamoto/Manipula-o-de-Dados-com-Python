import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import plotly.figure_factory as ff
import plotly.graph_objects as go

#carrega o conjunto de dados
df = pd.read_csv('/content/drive/MyDrive/ecommerce_estatistica.csv.csv')

#gráfico histograma
def grafico_histograma():
  return px.histogram(df, x='Nota', nbins=30, title='Histograma - Distribuição de Notas')

#gráfico de dispersão
def grafico_dispersao():
  fig = px.scatter(df, x='Preço', y='Nota', size='N_Avaliações', color='Qtd_Vendidos_Cod', hover_name='Marca', size_max=60, labels={'Qtd_Vendidos_Cod':'Quantidade Vendida'})
  fig.update_layout(
    title='Dispersão - Nota e Preço',
    xaxis_title='Preço',
    yaxis_title='Nota'
    )
  return fig

#mapa de calor
def grafico_mapa_de_calor():
  fig = go.Figure(data=go.Heatmap(z=df.values, x=['Nota', 'N_Avaliações', 'Preço', 'Qtd_Vendidos_Cod'], y=['Nota', 'N_Avaliações', 'Preço', 'Qtd_Vendidos_Cod'], colorscale='Viridis', colorbar=dict(title='Intensidade')))
  fig.update_layout(
    title='Correlações Nota, Nº de Avaliações, Preço e Qtd Vendidas',
    xaxis_title='Colunas',
    yaxis_title='Linhas'
    )
  return fig

#gráfico de barra
def grafico_barra():
  fig=px.bar(df, x='Temporada', y='Qtd_Vendidos_Cod', color='Nota', barmode='group', color_discrete_sequence=px.colors.sequential.Plasma)
  fig.update_layout(
      title='Quantidade Vendida por Temporada',
      xaxis_title='Temporada',
      yaxis_title='Quantidade Vendida',
      legend_title='Nota'
      )
  return fig

#gráfico de pizza
def grafico_pizza():
  return px.pie(df, names='Gênero', color='Gênero', hole=0.2, color_discrete_sequence=px.colors.sequential.RdBu, title='Distribuição de Produtos por Gênero')

#gráfico de densidade
def grafico_densidade():
  fig = ff.create_distplot([df['Preço']], group_labels=['Preço'], show_hist=False, show_rug=False)
  return fig

#gráfico de regressão
def grafico_regressao():
  fig = px.scatter(df, x='Preço', y='Qtd_Vendidos_Cod', trendline='ols', title='Relação entre Preço e Quantidade Vendida')
  fig.update_layout(
      xaxis_title='Preço',
      yaxis_title='Quantidade Vendida'
  )
  return fig

#função para cria todos os gráficos
def cria_graficos():
  fig1 = grafico_histograma()
  fig2 = grafico_dispersao()
  fig3 = grafico_mapa_de_calor()
  fig4 = grafico_barra()
  fig5 = grafico_pizza()
  fig6 = grafico_densidade()
  fig7 = grafico_regressao()
  return fig1, fig2, fig3, fig4, fig5, fig6, fig7

#cria app dash
def cria_app():
  app = Dash(__name__)

  fig1, fig2, fig3, fig4, fig5, fig6, fig7 = cria_graficos()

  app.layout = html.Div([
      dcc.Graph(figure=fig1),
      dcc.Graph(figure=fig2),
      dcc.Graph(figure=fig3),
      dcc.Graph(figure=fig4),
      dcc.Graph(figure=fig5),
      dcc.Graph(figure=fig6),
      dcc.Graph(figure=fig7)
  ])
  return app

if __name__ == '__main__':
  app = cria_app()
  app.run(debug=True, port=8050)