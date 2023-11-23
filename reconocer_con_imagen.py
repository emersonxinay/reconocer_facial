import cv2
import face_recognition

# Cargar la imagen de la persona que quieres reconocer
imagen_conocida = face_recognition.load_image_file("emerson.png")

# Codificar la imagen conocida
encoding_conocido = face_recognition.face_encodings(imagen_conocida)[0]

# Iniciar la cámara
camara = cv2.VideoCapture(0)

while True:
    # Leer el frame actual
    ret, frame = camara.read()

    # Convertir el frame a RGB
    rgb_frame = frame[:, :, ::-1]

    # Encontrar todas las caras en el frame actual
    encodings_desconocidos = face_recognition.face_encodings(rgb_frame)

    for encoding_desconocido in encodings_desconocidos:
        # Ver si las caras coinciden
        resultados = face_recognition.compare_faces([encoding_conocido], encoding_desconocido)

        # Dibujar un rectángulo alrededor de la cara
        if resultados[0]:
            (top, right, bottom, left) = face_recognition.face_locations(rgb_frame)[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Mostrar el resultado
    cv2.imshow('Video', frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()
