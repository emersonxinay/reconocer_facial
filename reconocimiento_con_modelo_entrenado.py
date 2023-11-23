import cv2
import numpy as np

# Cargar el modelo entrenado
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('modelo_entrenado.yml')  # Reemplaza 'modelo_entrenado.yml' con tu archivo de modelo entrenado

# Cargar el clasificador de detección de rostros pre-entrenado
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Obtener la región de interés (ROI) de la cara
        roi_gray = gray[y:y+h, x:x+w]

        # Realizar el reconocimiento facial
        id_, conf = recognizer.predict(roi_gray)

        # Definir nombres de las personas reconocidas
        if conf >= 45:  # Ajusta este umbral según la precisión de tu modelo
            font = cv2.FONT_HERSHEY_SIMPLEX
            nombre = "Emerson Espinoza"  # Cambia esto por los nombres correspondientes a tus etiquetas
            color = (255, 255, 255)  # Color del texto en BGR (blanco en este caso)
            grosor = 2
            cv2.putText(frame, nombre, (x, y), font, 1, color, grosor, cv2.LINE_AA)
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            desconocido = "Eres Desconocido"
            color = (255, 255, 255)
            grosor = 2
            cv2.putText(frame, desconocido, (x, y), font, 1, color, grosor, cv2.LINE_AA)

        # Dibujar un rectángulo alrededor del rostro
        color_rec = (255, 0, 0)  # Color del rectángulo en BGR (azul en este caso)
        grosor_rec = 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), color_rec, grosor_rec)

    cv2.imshow('Reconocimiento Facial', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
