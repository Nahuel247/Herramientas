
#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

# Funcionalidad:
# Herramienta para generar archivos GIF desde la camara del pc, un video o a partir de Screenshot de la pantalla

################################################
# IMPORTAMOS LAS LIBRERÍAS QUE VAMOS A UTILIZAR
################################################

import numpy as np
import cv2
import pyautogui
import imutils
import time
import imageio

##########################
# VARIABLES A DEFINIR
##########################

#PATH: ej. "C:/..../Proyecto/" Ruta en la que vamos a trabajar, aquí se guardará el GIF y es dónde debe estar el video que se desea cargar
#name_video: ej. "nombre_video.MP4", solo aplica si se va a trabajar con la opción 1
#nombre_guardado= ej,"prueba.gif", nombre del archivo de salida


#############################
# CONSTRUIMOS LA HERRAMIENTA
#############################

def crear_gif(origen):
    images=[]
    if(origen==1):  cap = cv2.VideoCapture(PATH + name_video)

    while True:
        if (origen == 0):
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=450)
        elif (origen == 1):
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=450)
        elif (origen == 2):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = imutils.resize(frame, width=1200)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            #time.sleep(2)
        else:
            print("origen no definido, valores sugeridos: 0,1,2")
            break

        # Mostramos en pantalla la captura y guardamos
        cv2.imshow("frame", frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        images.append(frame)
        kargs = {'duration': 1}
        imageio.mimsave(PATH+nombre_guardado,images,**kargs)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()


###############################
# IMPLEMENTAMOS LA HERRAMIENTA
###############################

crear_gif(0)
crear_gif(1)
crear_gif(2)

crear_gif(5)


###############
# REFERENCIAS:
###############

# https://www.youtube.com/watch?v=yy6KqVNmWYM
# https://datatofish.com/screenshot-python/
# https://stackoverflow.com/questions/38433425/custom-frame-duration-for-animated-gif-in-python-imageio
