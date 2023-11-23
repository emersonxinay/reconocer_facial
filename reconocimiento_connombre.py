import cv2

# Cargar el clasificador de detección de rostros pre-entrenado
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la cámara
cap = cv2.VideoCapture(0)

# Nombre a mostrar cuando se detecte el rostro
tu_nombre = "Rostro humano"

while True:
    # Capturar fotograma por fotograma
    ret, frame = cap.read()

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de los rostros detectados y mostrar el nombre
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Mostrar el nombre encima del rectángulo
        cv2.putText(frame, tu_nombre, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Mostrar el fotograma con los rostros detectados y el nombre
    cv2.imshow('Reconocimiento Facial', frame)

    # Salir del bucle cuando se presione 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
