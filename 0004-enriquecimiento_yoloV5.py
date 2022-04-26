
#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

# Funcionalidad:
# Herramienta para enriquecer la data para entrenar un modelo con YoloV5


################################################
# IMPORTAMOS LAS LIBRERÍAS QUE VAMOS A UTILIZAR
################################################

import os
import numpy as np
from matplotlib import pyplot as plt
import cv2
import glob
import random

from skimage.filters import gaussian
from skimage.util import random_noise
from skimage import img_as_ubyte
from skimage import color
import skimage
import skimage.io
import re
import shutil

#######################################
# DEFINIMOS RUTAS DE TRABAJO
#######################################

path_image= "C:/Users/.../images/*"
path_labels='.../labels/*'

path_image_val="C:/Users/.../images/val/"
path_image_train="C:/Users/.../images/train/"

path_labels_val="C:/Users/.../images/val/"
path_labels_train="C:/Users/.../images/train/"


#######################################
# DEFINIMOS FUNCIONES A UTILIZAR
#######################################

# Función para visualizar las imagenes
def show_image(image,cmap_type="gray"):
    plt.imshow(image,cmap=cmap_type)
    plt.show()

# ruido
def fun_ruido(img):
    noise_img=random_noise(img)
    #noise_img=noise_img.astype('uint8') * 255
    #noise_img=cv2.cvtColor(noise_img, cv2.COLOR_RGB2BGR)
    #cv2.imwrite(path[:-4]+"/smot/"+names_file[:-4]+"-noise"+".jpg", noise_img)
    skimage.io.imsave(path_image[:-1]+"/noise-"+re.sub("\.jpg|\.jpeg","",names_file)+".jpg",noise_img)

# bordes
def fun_bordes(img):
    from skimage import feature
    img_gray=color.rgb2gray(img)
    canny_edges=feature.canny(img_gray, sigma=0.5)
    #cv2.imwrite(path[:-4]+"/smot/"+names_file[:-4]+"-bordes"+".jpg", canny_edges)
    skimage.io.imsave(path_image[:-1]+"/bordes-"+re.sub("\.jpg|\.jpeg","",names_file)+".jpg",canny_edges)

# Segmentación (homogenización)
def fun_segmentation(img):
    from skimage.segmentation import slic
    from skimage.color import label2rgb
    segments=slic(img,n_segments=400)
    segmented_image=label2rgb(segments,img,kind='avg').astype(np.uint8)
    skimage.io.imsave(path_image[:-1]+"/segmented-"+re.sub("\.jpg|\.jpeg","",names_file)+".jpg",segmented_image)

# Clahe
def fun_clahe(img):    
    from skimage import exposure
    img_gray=color.rgb2gray(img)
    image_adapteq=exposure.equalize_adapthist(img_gray,clip_limit=0.5)
 #   show_image(image_adapteq)
    skimage.io.imsave(path_image[:-1]+"/clahe-"+re.sub("\.jpg|\.jpeg","",names_file)+".jpg",image_adapteq)

#Rotating
def fun_rotate(img,ang):
    from skimage.transform import rotate
    image_rotated = skimage.transform.rotate(img,ang, preserve_range=True).astype(np.uint8)
    skimage.io.imsave(path_image[:-1]+"/aumentation/"+names_file[:-4]+"-rotate"+".jpg", image_rotated)


#######################################
# INCREMENTAMOS/ENRIQUECEMOS LA DATA
#######################################

#TRABAJAMOS SOBRE LAS IMAGENES DUPLICANDO ARCHIVOS

#Enriquecemos la data, agregandole algún timo de modificación a las imagenes
for file in glob.glob(path_image):
    print(file)   # para ver el nombre de los archivos, incluye ruta, nombre del archivo y formato
    names_file= os.path.basename(file) # nombre del archivo
    img= cv2.imread(file)  # se lee cada imagen
    img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#   fun_bordes(img)
    fun_ruido(img)
#   fun_segmentation(img)
#   fun_rotate(img,9)
    fun_clahe(img)


# TRABAJAMOS SOBRE LAS ETIQUETAS DUPLICANDO ARCHIVOS

#Replicamos las etiquetas agregandole el tratamiento que recibió la imagen
for file in glob.glob(path_labels):
    names_file=os.path.basename(file)

#   shutil.copyfile(file, (path_labels[:-3] + '/bordes-' + names_file))
    shutil.copyfile(file,(path_labels[:-3]+'/noise-'+names_file))
#    shutil.copyfile(file, (path_labels[:-3] + '/segmented-' + names_file))
#    shutil.copyfile(file, (path_labels[:-3] + '/rotate-' + names_file))
    shutil.copyfile(file,(path_labels[:-3]+'/clahe-'+names_file))


#######################################################
# DISTRIBUIMOS LOS ARCHIVOS SEGÚN LO REQUIERE YOLOV5
#######################################################

#Creamos una lista que contengan el nombre de los archivos
list = []
for file in glob.glob(path_image):
    # print(file)   #just stop here to see all file names printed
    list.append(file)

# reordenamos los archivos
random.shuffle(list)

# creamos una muestra al azar
train = list[:int(len(list) * 0.9)]
val = list[int(len(list) * 0.9):]

# trasladamos las imagenes
for file in train:
    new_path = shutil.move(file, path_image_train)
    print(new_path)

for file in val:
    new_path = shutil.move(file, path_image_val)
    print(new_path)

# trasladamos los labels

for file in train:
    new_path = shutil.move(path_labels + re.sub("\.jpg|\.jpeg", '', os.path.basename(file)) + '.txt',
                           path_labels_train)
    print(new_path)

for file in val:
    new_path = shutil.move(path_labels + re.sub("\.jpg|\.jpeg", '', os.path.basename(file)) + '.txt',
                           path_labels_val)
    print(new_path)
