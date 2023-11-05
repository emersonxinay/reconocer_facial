from builtins import EncodingWarning
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import cv2
import dlib
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'fotos'
app.config['SECRET_KEY'] = 'clave_secreta'
socketio = SocketIO(app)

# Inicializar el detector de rostros de dlib
detector = dlib.get_frontal_face_detector()

# Inicializar la foto guardada (por defecto, estará vacía)
foto_guardada_encodings = None

@app.route('/')
def captura():
    return render_template('captura.html')

@app.route('/guardar_imagen', methods=['POST'])
def guardar_imagen():
    data = request.get_json()
    imagen_base64 = data['imagen'].split(',')[1]
    imagen_decodificada = base64.b64decode(imagen_base64)
    imagen_pil = Image.open(io.BytesIO(imagen_decodificada))
    imagen_np = np.array(imagen_pil)
    global foto_guardada_encodings
    foto_guardada_encodings = dlib.face_recognition_model_v1("shape_predictor_68_face_landmarks.dat")(imagen_np)
    return jsonify({'mensaje': 'Imagen capturada y guardada con éxito.'})

def reconocimiento_facial():
    global foto_guardada_encodings
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # Capturar frame por frame

        # Detectar rostros en el frame
        faces = detector(frame)
        
        # Encodings del rostro en el frame
        for face in faces:
            encodings = dlib.face_recognition_model_v1("shape_predictor_68_face_landmarks.dat")(frame, face)

            # Comparar los encodings del rostro con la foto guardada
            if foto_guardada_encodings is not None:
                match = dlib.vector_matching_embeddings(foto_guardada_encodings, np.array([EncodingWarning]))
                # Dibujar el resultado en el frame
                if match and match[0] > 0.6:  # Umbral de confianza (ajustar según sea necesario)
                    mensaje = "¡Coincidencia!"
                else:
                    mensaje = "No Coincide"
            else:
                mensaje = "No hay foto guardada para comparar."

            socketio.emit('mensaje', mensaje)

        # Salir del bucle cuando se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara
    cap.release()

if __name__ == '__main__':
    # Iniciar el hilo de reconocimiento facial
    socketio.start_background_task(target=reconocimiento_facial)
    # Iniciar el servidor de desarrollo Flask con SocketIO
    socketio.run(app, debug=True)
