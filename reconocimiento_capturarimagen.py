import cv2
import os

# Directorio donde se guardarán las imágenes
dir_nombre = 'dataset'  # Cambia esto por el nombre de tu directorio

# Crea el directorio si no existe
if not os.path.exists(dir_nombre):
    os.makedirs(dir_nombre)

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Contador para etiquetar las imágenes
contador = 0

while contador < 100:  # Puedes ajustar la cantidad de imágenes a capturar
    ret, frame = cap.read()

    # Mostrar el fotograma actual
    cv2.imshow('Captura de Imágenes', frame)

    # Guardar la imagen capturada en el directorio
    img_nombre = f'{dir_nombre}/imagen_{contador}.jpg'
    cv2.imwrite(img_nombre, frame)

    # Aumentar el contador
    contador += 1

    # Esperar a que se presione la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
