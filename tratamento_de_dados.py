# -*- coding: utf-8 -*-
"""Tratamento de Dados.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JYI4dbv6rg0gQ5d6vuDNWr8-Z7IeNkBl
"""

#importacado do arquivo com os dados
import pandas as pd

df = pd.read_csv('/content/Drive/MyDrive/ecommerce.csv', encoding='utf-8')

#Verificações inicias do arquivo de dados
print('Verificar a qtd de Linhas e colunas: ', df.shape)
print('Verificar Tipagem:\n', df.dtypes)
print('Verificar valores nulos:\n', df.isnull().sum())

#Substitui os valores nulos das colunas ‘Temporada’ e ‘Marca’ por ‘Não Definido’
df.fillna({'Temporada':'Não Definido'}, inplace=True)
df.fillna({'Marca':'Não Definido'}, inplace=True)

#Converte colunas 'Marca', 'Material' e 'Temporada' para letras minúsculas
df['Marca'] = df['Marca'].str.lower()
df['Material'] = df['Material'].str.lower()
df['Temporada'] = df['Temporada'].str.lower()

#Retira linhas duplicadas e retira linhas com menos de 8 valores não nulos
df.drop_duplicates()
df = df.dropna(thresh=8)

#Cálculo do intervalo interquartil (IQR)
q1 = df['N_Avaliacoes'].quantile(0.25)
q3 = df['N_Avaliacoes'].quantile(0.75)
iqr = q3 - q1

#Definição do limite superior
limite_alto = q3 + 1.5 * iqr

#Filtra produtos que possuem um número de avaliações maior que o limite superior
df_avaliados = df[df['N_Avaliacoes'] > limite_alto]

#Tratamento da coluna 'Condicao
df['Condicao_Atual'] = df['Condicao'].apply(lambda x: x.split(' ')[0].strip())
df['Qtd_Vendidos'] = df['Condicao'].apply(lambda x: x.split(' ')[4].strip() if len(x.split(' ')) > 4 else 'Nenhum')

#Tratamento do campo desconto
df['Desconto'] = df['Desconto'].astype(str)
df['Desconto'] = df['Desconto'].apply(lambda x: x.split('%')[0].strip())

#Salva o dataframe em novo arquivo
df.to_csv('/content/Drive/MyDrive/ecommerce_tratado.csv', index=False)