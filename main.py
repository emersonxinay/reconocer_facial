from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = None
camera_enabled = False

def init_camera():
    global camera
    camera = cv2.VideoCapture(0)

def generate_frames():
    global camera_enabled
    while camera_enabled:
        success, frame = camera.read()
        if not success:
            print("Error al leer el fotograma. ¡Deteniendo la captura!")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', camera_enabled=camera_enabled)

@app.route('/toggle_camera')
def toggle_camera():
    global camera_enabled
    if camera_enabled:
        camera_enabled = False
    else:
        init_camera()
        camera_enabled = True
    return "Camera toggled"

@app.route('/video_feed')
def video_feed():
    if camera_enabled:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera is disabled"

if __name__ == '__main__':
    app.run(debug=True)
