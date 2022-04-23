
#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

# Funcionalidad:
# Herramienta para estimar la tasa de incumplimiento
# según grupo


# Variables por definir:
#Var_exp: Arreglo con Variable continua o categorica
#Var_resp: Arreglo con Variable respuesta, esta debe ser 0 o 1
#n_tramos: Número de grupos en los que se tramará una variable continua, de ser categorica no aplica


# Importamos librerias
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from numpy.random import rand
from plotly.subplots import make_subplots


# Definimos función para crear bivariantes
def bivariante(var_exp, var_resp, n_tramos):
    if(var_exp.dtypes!="object"):
        # Tramamos la variable explicativa en n_tramos
        bins = list(sorted(set(np.quantile(var_exp.copy(), np.arange(0,1+(1/n_tramos),1/n_tramos),overwrite_input=True))))
        labels = [f'{round(i,3)}-{round(j,3)}' for i, j in zip(bins[:-1], bins[1:])] # creamos etiquetas
        categorias = pd.cut(var_exp, bins=bins, labels=labels, include_lowest=True, right=True)
        df=pd.DataFrame({'var_exp':var_exp,'categorias':categorias,'var_resp':var_resp})
        # agrupamos para conocer la tasa de incumplimiento según tramo
        df_group= df.groupby('categorias').agg(tasa_malo=('var_resp', np.mean), n=('categorias', len)).reset_index()
    else:
        df = pd.DataFrame({'categorias': var_exp, 'var_resp': var_resp})
        df_group = df.groupby('categorias').agg(tasa_malo=('var_resp', np.mean), n=('categorias', len)).reset_index()

    #graficamos
    trace1 = go.Bar(x=df_group['categorias'], y=df_group['n'], name="Número de registros (N)",
                    marker=dict(color='rgb(34,163,192)'))
    trace2 = go.Scatter(x=df_group['categorias'], y=df_group['tasa_malo'], name="Tasa de incumplimiento",
        yaxis='y2')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2,secondary_y=True)
    fig['layout'].update(height = 600, width = 800, title = "Tasa de incumplimiento según " + var_exp.name,
                         xaxis=dict(tickangle=-45, title =var_exp.name),
                         yaxis=dict(title ="Número de registros (N)"),
                         yaxis2=dict(title='Tasa de incumplimiento'),
                         legend=dict(
                             orientation="h",
                             yanchor="bottom",
                             y=1.02,
                             xanchor="right",
                             x=1
                         ))

    #fig.show() # Para visualizar en html
    #fig.write_html(var_exp.name+'.html', auto_open=True) # Para visualizar y guardar en html
    fig.write_image(var_exp.name+".jpg") # Para guardar en JPG



##################################
# Implementamos la función creada
##################################

EDAD=np.round(rand(1000)*80) +18
SEXO=np.random.choice(a=["M","H"],size=1000)
INCUMPLIMIENTO=np.round((np.array(1-EDAD/100) + np.array(rand(1000)))/2) #Incumplimiento como f() de la edad


data=pd.DataFrame({'EDAD':EDAD,'SEXO':SEXO,'VAR_RESP':INCUMPLIMIENTO})

# Ejecutamos la función
bivariante(data['EDAD'],data['VAR_RESP'],10)
bivariante(data['SEXO'],data['VAR_RESP'],10)