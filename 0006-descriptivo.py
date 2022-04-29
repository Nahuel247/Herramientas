
#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

# Funcionalidad:
# Herramienta para generar análisis descriptivo de la data

################################################
# IMPORTAMOS LAS LIBRERÍAS QUE VAMOS A UTILIZAR
################################################

import pandas as pd
import numpy as np
from pandas import ExcelWriter
from numpy.random import rand


#############################
# CONSTRUIMOS LA HERRAMIENTA
#############################

# Definimos una función para procesar una variable categórica
def descriptivo_texto(data,names_column):
    frec = np.unique(data[[names_column]], return_counts=True)
    df = pd.DataFrame(frec).T.copy()
    observaciones=np.nan
    df[observaciones]=np.nan
    df.columns = ["categorías", "frecuencia","observaciones"]
    return df

# Definimos una función para procesar una variable númericas
def descriptivo_num (data, names_column):
    array=data[[names_column]]
    n_zeros = np.sum([array==0]) # N° de ceros
    n_negativos=np.sum([array<0]) # N° de valores negativos
    n_missing=array[np.isnan(array)].sum()[0] # N° de valores missing
    min= array[~np.isnan(array)].min()[0]
    max= array[~np.isnan(array)].max()[0]
    mean= array[~np.isnan(array)].mean()[0]
    p5=np.percentile(array[~np.isnan(array)], 5) # Valor del percentil al 5%
    p10 = np.percentile(array[~np.isnan(array)], 10)
    p25 = np.percentile(array[~np.isnan(array)], 25)
    p50 = np.percentile(array[~np.isnan(array)], 50)
    p75 = np.percentile(array[~np.isnan(array)], 75)
    p90 = np.percentile(array[~np.isnan(array)], 90)
    observaciones=np.nan
    df=pd.DataFrame([{"n_ceros":n_zeros, "n_negativos": n_negativos,
                      "n_missing":n_missing,"min":min,"max":max, "mean":mean,
                      "p5":p5,"p10":p10,"p25":p25,"p50":p50,"p75":p75,"p90":p90,
                      "observaciones": observaciones}]).T
    df.columns=[names_column]
    return df

# construimos una función para gestionar una base de datos con registros categoricos o númericos
def descriptivo(data):
    with ExcelWriter("Descriptivo.xlsx") as writer:
        names_column_num = data.loc[:, (data.dtypes != "object")].columns.copy()
        names_column_text = data.loc[:, (data.dtypes == "object")].columns.copy()
        n = 0
        if (names_column_num.shape[0] >= 1):
            desc_num_list = []
            for names_column in names_column_num:
                desc_num = descriptivo_num(data, names_column)
                desc_num_list.append(desc_num)
            final_desc_num = pd.concat(desc_num_list, axis=1).T
            final_desc_num.to_excel(writer, "var_numericas")
            n += 1

        if (names_column_text.shape[0] >= 1):
            for names_column in names_column_text:
                n = n + 1
                desc_txt = descriptivo_texto(data, names_column)
                desc_txt.to_excel(writer, names_column, index=False)
    print("Se ha creado un descriptivo de los datos")


###############################
# IMPLEMENTAMOS LA HERRAMIENTA
###############################

# creamos un set de datos para hacer pruebas
EDAD=np.round(rand(1000)*80) +18
TIEMPO_EMPRESA=np.round(rand(1000)*80)-4
SEXO=np.random.choice(a=["M","H"],size=1000)
SEXO[[1,100,340]]="F"
CATEGORIA=np.random.choice(a=["A","B"],size=1000)

data=pd.DataFrame({'EDAD':EDAD,'TIEMPO_EMPRESA':TIEMPO_EMPRESA,'SEXO':SEXO,'CATEGORÍA':CATEGORIA})
data.head()

descriptivo(data)

####################
# REFERENCIAS
####################

# https://stackoverflow.com/questions/14225676/save-list-of-dataframes-to-multisheet-excel-spreadsheet