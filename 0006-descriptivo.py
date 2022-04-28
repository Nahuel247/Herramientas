
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

def descriptivo_texto(data,names_column):
    frec = np.unique(data[[names_column]], return_counts=True)
    df = pd.DataFrame(frec).T.copy()
    observaciones=np.nan
    df[observaciones]=observaciones
    df.columns = ["categorías", "frecuencia","observaciones"]
    return df

descriptivo_texto(data, "SEXO")


def descriptivo_num (data, names_column):
    array=data[[names_column]]
    n_zeros = np.sum([array==0])
    n_negativos=np.sum([array<0])
    n_missing=array[np.isnan(array)].sum()[0]
    min= array[~np.isnan(array)].min()[0]
    max= array[~np.isnan(array)].max()[0]
    mean= array[~np.isnan(array)].mean()[0]
    p5=np.percentile(array[~np.isnan(array)], 5)
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


def descriptivo(data):
    with ExcelWriter("Descriptivo.xlsx") as writer:
        data_num = data.loc[:, (data.dtypes != "object")].copy()
        data_text = data.loc[:, (data.dtypes == "object")].copy()
        n = 0
        if (data_num.shape[1] >= 1):
            pred_list = []
            list_var = data_num.columns
            for names_column in list_var:
                if (data[[names_column]].dtypes != "object").all():
                    prediction = pd.DataFrame(descriptivo_num(data, names_column))
                    pred_list.append(prediction)
            final_prediction = pd.concat(pred_list, axis=1).T
            final_prediction.to_excel(writer, names_column)
            n += 1

        if (data_text.shape[1] >= 1):
            list_dfs = data_text.columns
            for names_column in list_dfs:
                n = n + 1
                df = descriptivo_texto(data_text, names_column)
                df.columns = ["categorías", "frecuencia","observaciones"]
                df.to_excel(writer, names_column, index=False)
    print("Se ha creado un descriptivo de los datos")


###############################
# IMPLEMENTAMOS LA HERRAMIENTA
###############################

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