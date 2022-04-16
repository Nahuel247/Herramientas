#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

# Funcionalidad:
# Herramienta para producir múltiples bivariantes, se requiere ya haber ejecutado el archivo "0001-bivariantes"
# Además deben asegurarse que esté activada la línea para guardar los gráficos como "jpg"

# Variables por definir:
#data: base de datos con las variables de interés y la variable respuesta
#Variables: array con un listado de variables de interés
#var_resp: string con el nombre de la variable respuesta
#n_tramos: Número de veces en que será tramada una variable categorica


def multiples_bivariantes(data, variables, var_resp,n_tramos):
    for x in variables:
        bivariante(data[x],data[var_resp],n_tramos)
        print(x)


##################################
# Implementamos la función creada
##################################

EDAD=np.round(rand(1000)*80) +18
SEXO=np.random.choice(a=["M","H"],size=1000)
INCUMPLIMIENTO=np.round((np.array(1-EDAD/100) + np.array(rand(1000)))/2) #Incumplimiento como f() de la edad


data=pd.DataFrame({'EDAD':EDAD,'SEXO':SEXO,'VAR_RESP':INCUMPLIMIENTO})

# Ejecutamos la función
variables=["EDAD","SEXO"]
var_resp="VAR_RESP"
n_tramos=10

multiples_bivariantes(data, variables, var_resp,n_tramos)



