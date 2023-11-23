from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Cargar el modelo entrenado
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('modelo_entrenado.yml')  # Reemplaza 'modelo_entrenado.yml' con tu archivo de modelo entrenado

# Cargar el clasificador de detección de rostros pre-entrenado
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la cámara
cap = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                id_, conf = recognizer.predict(roi_gray)
                if conf >= 45:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    nombre = "Tu Nombre"  # Cambia esto por los nombres correspondientes a tus etiquetas
                    color = (255, 255, 255)
                    grosor = 2
                    cv2.putText(frame, nombre, (x, y), font, 1, color, grosor, cv2.LINE_AA)

                color_rec = (255, 0, 0)
                grosor_rec = 2
                cv2.rectangle(frame, (x, y), (x+w, y+h), color_rec, grosor_rec)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('rec_facial.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
