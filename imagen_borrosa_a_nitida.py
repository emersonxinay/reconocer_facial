import cv2 
from flask import Flask, request, render_template, send_file, send_from_directory
import os
import numpy as np
import pytesseract
app = Flask(__name__)

# Configuración para Tesseract y OpenCV
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imagen = request.files['imagen']
        
        # Guardar la imagen en el servidor
        imagen_path = os.path.join('uploads', imagen.filename)
        imagen.save(imagen_path)
        
        # Leer la imagen con OpenCV
        img = cv2.imread(imagen_path)
        
        # Aplicar mejora de nitidez utilizando el filtro de aumento de nitidez de OpenCV
        img_nitida = cv2.filter2D(img, -1, sharpening_kernel)
        
        # Guardar la imagen mejorada en el servidor
        imagen_nitida_path = os.path.join('uploads', 'imagen_nitida.png')
        cv2.imwrite(imagen_nitida_path, img_nitida)
        
        # Eliminar la imagen cargada del servidor
        os.remove(imagen_path)
        
        # Servir la imagen mejorada como respuesta
        return send_file(imagen_nitida_path, mimetype='image/png', as_attachment=True, download_name='imagen_nitida.png')

    return render_template('borrosa.html')

# Filtro de aumento de nitidez
sharpening_kernel = np.array([[-1, -1, -1],
                              [-1, 9, -1],
                              [-1, -1, -1]])

if __name__ == '__main__':
    app.run(debug=True)
