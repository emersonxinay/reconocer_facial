# esto es solo para una carpeta y solo un usuario
import cv2
import numpy as np
import os

# Directorio donde se encuentran las imágenes capturadas
dir_nombre = 'dataset'  # Cambia esto por el nombre de tu directorio

def cargar_imagenes_y_etiquetas(dir_nombre):
    imagenes = []
    etiquetas = []

    for file in os.listdir(dir_nombre):
        if file.endswith("jpg"):
            path = os.path.join(dir_nombre, file)
            imagen = cv2.imread(path, 0)  # Leer en escala de grises
            if imagen is not None:
                print(f'Imagen {file} cargada correctamente')
                imagenes.append(imagen)
                etiquetas.append(0)  # Asignar etiqueta única '0' para todas las imágenes
            else:
                print(f'¡Error al cargar la imagen {file}!')

    return imagenes, etiquetas

# Obtener las imágenes y las etiquetas
imagenes, etiquetas = cargar_imagenes_y_etiquetas(dir_nombre)
print(f'Total de imágenes cargadas: {len(imagenes)}')

# Crear el clasificador LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenar el clasificador
if len(imagenes) > 0:
    recognizer.train(imagenes, np.array(etiquetas))
    print('Clasificador entrenado exitosamente')
    # Guardar el modelo entrenado
    recognizer.save('modelo_entrenado.yml')
else:
    print('Error: No se pudo entrenar el clasificador debido a un problema con los datos')
