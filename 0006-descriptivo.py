
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
np.random.seed(0)


#############################
# CONSTRUIMOS LA HERRAMIENTA
#############################

# Función para analizar variables numéricas
def descriptivo_num(data, col):
    serie = data[col]
    array = serie.dropna().values
    stats = {
        "n_ceros": np.count_nonzero(array == 0),
        "n_negativos": np.count_nonzero(array < 0),
        "n_missing": serie.isna().sum(),
        "min": np.min(array) if len(array) > 0 else np.nan,
        "max": np.max(array) if len(array) > 0 else np.nan,
        "mean": np.mean(array) if len(array) > 0 else np.nan,
        "p5": np.percentile(array, 5) if len(array) > 0 else np.nan,
        "p10": np.percentile(array, 10) if len(array) > 0 else np.nan,
        "p25": np.percentile(array, 25) if len(array) > 0 else np.nan,
        "p50": np.percentile(array, 50) if len(array) > 0 else np.nan,
        "p75": np.percentile(array, 75) if len(array) > 0 else np.nan,
        "p90": np.percentile(array, 90) if len(array) > 0 else np.nan,
        "observaciones": np.nan
    }
    return pd.DataFrame(stats, index=[col]).T


# Función para analizar fechas (igual que numéricas pero adaptado)
def descriptivo_fecha(data, col):
    serie = pd.to_datetime(data[col], errors='coerce')
    serie_no_na = serie.dropna()
    stats = {
        "n_ceros": 0,
        "n_negativos": 0,
        "n_missing": serie.isna().sum(),
        "min": serie_no_na.min() if not serie_no_na.empty else np.nan,
        "max": serie_no_na.max() if not serie_no_na.empty else np.nan,
        "mean": serie_no_na.mean() if not serie_no_na.empty else np.nan,
        "p5": serie_no_na.quantile(0.05) if not serie_no_na.empty else np.nan,
        "p10": serie_no_na.quantile(0.10) if not serie_no_na.empty else np.nan,
        "p25": serie_no_na.quantile(0.25) if not serie_no_na.empty else np.nan,
        "p50": serie_no_na.quantile(0.50) if not serie_no_na.empty else np.nan,
        "p75": serie_no_na.quantile(0.75) if not serie_no_na.empty else np.nan,
        "p90": serie_no_na.quantile(0.90) if not serie_no_na.empty else np.nan,
        "observaciones": np.nan
    }
    return pd.DataFrame(stats, index=[col]).T

# Función para analizar variables categóricas
def descriptivo_texto(data, col):
    frec = data[col].value_counts(dropna=False).reset_index()
    frec.columns = ["categoría", "frecuencia"]
    frec["observaciones"] = np.nan
    return frec


# Función principal
def descriptivo(data):
    with ExcelWriter("Descriptivo.xlsx") as writer:
        cols_num = data.select_dtypes(include=[np.number]).columns
        cols_cat = data.select_dtypes(include=["object", "category"]).columns
        cols_fecha = data.select_dtypes(include=["datetime64[ns]"]).columns

        desc_numerico = []
        for col in cols_num:
            desc_numerico.append(descriptivo_num(data, col))

        for col in cols_fecha:
            desc_numerico.append(descriptivo_fecha(data, col))

        if desc_numerico:
            df_num = pd.concat(desc_numerico, axis=1).T
            df_num.to_excel(writer, sheet_name="var_numericas")

        for col in cols_cat:
            df_cat = descriptivo_texto(data, col)
            df_cat.to_excel(writer, sheet_name=f"cat_{col}", index=False)

    print("Se ha creado un descriptivo")



###############################
# IMPLEMENTAMOS LA HERRAMIENTA
###############################
# Crear un DataFrame de ejemplo

df = pd.DataFrame({
    "timestamp": pd.date_range(start="2023-05-01", periods=100, freq="D").tolist(),
    "latency": np.random.uniform(10, 200, 100).round(2),
    "signal_strength": np.random.normal(-90, 5, 100).round(2),
    "locality": np.random.choice(["Centro", "Norte", "Sur", "Este", "Oeste"], size=100)
})

# Introducir valores nulos y extremos
df.loc[5, "latency"] = 0
df.loc[10, "signal_strength"] = -120
df.loc[15, "latency"] = np.nan
df.loc[20, "timestamp"] = pd.NaT

print(df.head())


####################
# REFERENCIAS
####################

# https://stackoverflow.com/questions/14225676/save-list-of-dataframes-to-multisheet-excel-spreadsheet
