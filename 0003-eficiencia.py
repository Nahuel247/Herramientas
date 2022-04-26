
#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

# Funcionalidad:
# Herramienta para visualizar la eficiencia de una variable para discretizar a clientes que cumplen de los que incumplen


# Variables por definir:
#marca_malo: Variable respuesta del cliente (real), esta debe ser 0 (cumplen) o 1 (incumplimiento)
#Var_exp: Probabilidad de incumplimiento por el modelo, valor entre 0 y 1 o variable continua de interés
#n_tramos: Número de grupos en los que se tramará una variable continua, de ser categorica no aplica


# Importamos librerias
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from scipy.stats import beta
import random
from itertools import chain


def eficiencia(var_exp, marca_malo, n_tramos):
    bins = list(sorted(set(np.quantile(var_exp.copy(), np.arange(0,1+(1/n_tramos),1/n_tramos),overwrite_input=True))))
    labels = [f'{round(j,3)}-{round(i,3)}' for i, j in zip(bins[:-1], bins[1:])] # creamos etiquetas
    categorias = pd.cut(var_exp, bins=bins, labels=labels, include_lowest=True, right=True)
    df=pd.DataFrame({'var_exp':var_exp,'probabilidad_incumplimiento':categorias,'marca_malo':marca_malo})
    df['cumple'] = df['marca_malo'].apply(lambda x: 1 if x == 0 else 0)
    # agrupamos para conocer la tasa de incumplimiento según tramo

    df_group= df.groupby('probabilidad_incumplimiento').agg(tasa_malo=('marca_malo', np.mean),
                                                        cumplen=('cumple',np.sum),incumplen=('marca_malo', np.sum),
                                                        n=('probabilidad_incumplimiento', len)
                                                        ).reset_index()

    df_group=df_group.assign(veintil=range(np.shape(df_group)[0],0,-1))
    df_group=df_group.sort_values('veintil', ascending=True).copy()
    df_group=df_group.assign(grupo=1)
    df_group['malos_acumulado'] = df_group.groupby(['grupo'])['incumplen'].cumsum()/np.sum(df_group['incumplen'])

    #graficamos
    trace1=go.Bar(
        x=df_group['probabilidad_incumplimiento'],
        y=df_group['incumplen'], name='incumplen',marker=dict(color='rgb(227, 57, 20)'))

    trace2=go.Bar(
        x=df_group['probabilidad_incumplimiento'],
        y=df_group['cumplen'], name='cumplen',marker=dict(color='rgb(31, 52, 204)'))

    trace3= go.Scatter(
        x=df_group['probabilidad_incumplimiento'],
        y=df_group["malos_acumulado"],name='tasa de incumplimiento acumulada',
        yaxis='y2',
        mode='lines+markers+text',
        text=round(df_group["malos_acumulado"],2), textposition="top center",
        textfont=dict(family="sans serif", size=18, color="black"))

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_layout(barmode='stack')

    fig.add_trace(trace3)
    fig['layout'].update(height = 600, width = 800, title = "Tasa de incumplimiento según " + var_exp.name,
                         xaxis=dict(tickangle=-45, title =var_exp.name),
                         yaxis=dict(title ="Número de registros (N)"),
                         yaxis2=dict(title='Tasa de incumplimiento acumulada'),
                         legend=dict(
                             orientation="h",
                             yanchor="bottom",
                             y=1.02,
                             xanchor="right",
                             x=1
                         ))
    # fig.show() # Para visualizar en html
    # fig.write_html(var_exp.name+'.html', auto_open=True) # Para visualizar y guardar en html
    fig.write_image(var_exp.name + ".jpg")  # Para guardar en JPG


##################################
# Implementamos la función creada
##################################

# Generamos un set de datos de prueba
a, b = 10, 2
x_valores = np.linspace(beta.ppf(0.01, a, b),beta.ppf(1, a, b), 1000)
samplelist=[0,1]
MARCA_MALO=[random.choices(samplelist, cum_weights=((1-i)*100,i*100)) for i in x_valores]   # Marca de incumplimiento del cliente (0 = cumple, 1 = incumple)]
MARCA_MALO=list(chain.from_iterable(MARCA_MALO))
PROBABILIDAD=x_valores.copy() # Probabilidad de incumplimiento predicha por el modelo

data=pd.DataFrame({'PROBABILIDAD':PROBABILIDAD,'MARCA_MALO':MARCA_MALO})

# Ejecutamos la función
eficiencia(data['PROBABILIDAD'],data['MARCA_MALO'],10)
