# bibliotecas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.plotting.backend = "plotly"

# - coleta de dados; > Data Set da plaataforma kaggle disponivel em:  https://www.kaggle.com/datasets/renangomes/dengue-temperatura-e-chuvas-em-campinassp
df_dengue = pd.read_csv('./cases_dengue.csv', delimiter = ',')

# separando a data entre ano e mes
df_dengue['data'] = pd.to_datetime(df_dengue['data'])
df_dengue['ano'] = df_dengue['data'].dt.year
df_dengue['mes'] = df_dengue['data'].dt.month_name()
df_dengue ['ano'] = pd.to_numeric(df_dengue['ano'])

#renomeando e reordenando colunas
df_dengue.rename(columns={'casos-confirmados':'casos_confirmados','chuva':'volume_chuva', 'temperatura-media': 'temperatura_media','temperatura-mininima': 'temperatura_minima', 'temperatura-maxima': 'temperatura_maxima'}, inplace= True)
df_dengue = df_dengue[['ano', 'mes', 'casos_confirmados', 'volume_chuva','temperatura_media','temperatura_minima', 'temperatura_maxima']]

# média de volume de chuva por ano e mês
#transform() permite aplicar a funcao media a cada valor do agrupamento
media_por_ano_mes = df_dengue.groupby('mes')['volume_chuva'].transform('mean')

# substituir os valores nulos pela média por ano e mês
df_dengue['volume_chuva'] = df_dengue['volume_chuva'].fillna(media_por_ano_mes).round()

##Visualizaçoes 

sns.set(rc={'figure.figsize':(12,8)}) # dimensões para o grafico

#  total de caso em anos
casos_anos = df_dengue[['ano', 'casos_confirmados']].groupby('ano').agg('sum')

# Grafico 01 - visualizacao do total a cada ano da serie
with sns.axes_style('darkgrid'):
  graf_01 = sns.barplot(data = casos_anos, x ='ano', y ='casos_confirmados', ci = None, palette = 'dark')
  graf_01.set(title = "Casos Confirmados de Dengue em Campinas - SP (1998 - 2014)", xlabel= 'Ano', ylabel = 'Quantidade')
  plt.xticks(rotation=45)
  #adiciona valores a cada coluna
  for i in graf_01.patches:
    graf_01.annotate(i.get_height(),
                            (i.get_x()+ i.get_width() / 2, i.get_height()),
                            ha='center', va = 'baseline', fontsize = 8,
                            color= 'black', xytext=(0,1),
                            textcoords = 'offset pixels')

  graf_01.fifure.savefig('graf_01')

# grafico 02 visualizacao do total a cada mes da serie
df_months= df_dengue[['mes','casos_confirmados']].groupby('mes').agg('sum')
df_months = df_months.sort_values(by='casos_confirmados' )
with sns.axes_style('darkgrid'):
  graf_02= sns.barplot(data = df_months, x ='mes', y ='casos_confirmados', ci = None, palette = 'dark')
  graf_02.set(title = "Total de Casos de Dengue Durante os Meses em Campinas - SP (1998 - 2014)", xlabel= 'Ano', ylabel = 'Número de Casos')
  plt.xticks(rotation=45)

  #adiciona valores a cada coluna
  for i in graf_02.patches:
    graf_02.annotate(i.get_height(),
                            (i.get_x()+ i.get_width() / 2, i.get_height()),
                            ha='center', va = 'baseline', fontsize = 8,
                            color= 'black', xytext=(0,1),
                            textcoords = 'offset pixels')
  
  graf_02.figure.savefig('graf_02')

# filtro dos anos extremos menor(2004) e maior quantidade de casos(2014)
df_years = df_dengue[df_dengue['ano'].isin([2004, 2014])]
df_y04 = df_dengue[df_dengue['ano'].isin([2004])]
df_y14 = df_dengue[df_dengue['ano'].isin([2014])]

#grafico 03 total de casos em 2004
graf_03 = plt.figure(figsize = ( 12, 8 ))
plt.scatter( x = 'mes' , y = 'casos_confirmados', data = df_y04)
plt.xlabel( 'Meses' , size = 12)
plt.xticks(rotation=45)
plt.ylabel( 'Quantidade de casos' , size = 12 )
plt.title( 'Casos de Dengue nos Meses de 2004 em Campinas - SP' , size = 14 )

graf_03.figure.savefig('graf_03')

#grafico 04 total de casos em 2014
graf_04 = plt.figure(figsize = ( 12, 8 ))
plt.scatter( x = 'mes' , y = 'casos_confirmados', data = df_y14)
plt.xlabel( 'Meses' , size = 12)
plt.xticks(rotation=45)
plt.ylabel( 'Quantidade de casos' , size = 12 )
plt.title( 'Casos de Dengue nos Meses de 2014 em Campinas - SP' , size = 14 )

graf_04.figure.savefig('graf_04')

#df com os dois anos agrupados em 
df_04_14 = df_years.groupby(['ano', 'mes'])['casos_confirmados'].sum().reset_index().pivot('mes', 'ano', 'casos_confirmados')

#juntando os dois graficos anteriores em um gráfico  interativo
fig = df_04_14.plot(kind='barh', title="Casos confirmados de dengue em Campinas para os anos de 2004 e 2014")
# Define o nome dos eixos
fig.update_layout(xaxis_title='Número de casos confirmados', yaxis_title='Mês')
#centraliza o titulo
fig.update_layout(title_x=0.5)

# variacao da chuva nos dois anos 04/14
with sns.axes_style('darkgrid'):
  graf_05 = sns.lineplot(data=df_years, x='mes', y='volume_chuva', hue='ano', palette='dark')
  plt.xticks(rotation=45)
  graf_05.set(title='Média de Chuva  Em Campinas - SP - 2004 e 2014', xlabel='Meses', ylabel='Volume em (mm)');
  graf_05.get_legend().set_title("Ano");
  graf_05.figure.savefig('graf_05')

#variacao datemperatura nos dois anos 04/14
with sns.axes_style('darkgrid'):

  graf_06 = sns.lineplot(data=df_years, x='mes', y='temperatura_media', hue='ano', palette='dark')
  graf_06.set(title='Média Temperatura Em campinas-SP - 2004 e 2014', xlabel='Meses', ylabel='Temperatura (°C)')
  plt.xticks(rotation=45)
  graf_06.get_legend().set_title("Ano");
  graf_06.figure.savefig('graf_06')











