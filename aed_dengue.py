# bibliotecas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.plotting.backend = "plotly"

# - coleta de dados; > Data Set da plaataforma kaggle disponivel em:  https://www.kaggle.com/datasets/renangomes/dengue-temperatura-e-chuvas-em-campinassp
df_dengue = pd.read_csv('./cases_dengue.csv', delimiter = ',')
df_dengue.tail()