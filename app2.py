# Importamos librerias
from flask import Flask, render_template, Response, redirect, request
import cv2
import mediapipe as mp
import io
import face_recognition

# Inicializamos Mediapipe y la Videocaptura
mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)
mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)
cap = cv2.VideoCapture(0)

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Variable para almacenar la imagen de referencia
reference_image = None

# Función para generar frames del video en tiempo real
def gen_frame():
    global reference_image
    
    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        # Convertir el frame a RGB para face_recognition
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if reference_image is not None:
            # Encuentra los encodings de rostro en la imagen de referencia
            reference_face_encoding = face_recognition.face_encodings(reference_image)[0]

            # Encuentra los encodings de rostro en el frame actual
            face_locations = face_recognition.face_locations(frame_rgb)
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

            # Compara los encodings de rostro para determinar si es la misma persona
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces([reference_face_encoding], face_encoding)
                if True in matches:
                    # Si hay una coincidencia, dibuja un rectángulo verde alrededor del rostro
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Procesar el frame con Mediapipe
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = MallaFacial.process(frameRGB)

        if resultados.multi_face_landmarks:
            for rostros in resultados.multi_face_landmarks:
                mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACEMESH_TESSELATION, ConfDibu, ConfDibu)

        # Codificar el frame en Bytes
        success, encode = cv2.imencode('.jpg', frame)
        frame = encode.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Ruta principal
@app.route('/')
def index():
    return render_template('index2.html')

# Ruta para cargar la imagen de referencia
@app.route('/load', methods=['POST'])
def load():
    global reference_image
    file = request.files['image']
    if file:
        image = file.read()
        reference_image = face_recognition.load_image_file(io.BytesIO(image))
    return redirect('/')

# Ruta del video
@app.route('/video')
def video():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
