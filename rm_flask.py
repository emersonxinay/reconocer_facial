from flask import Flask, request, render_template, send_file
import os
import pytesseract
from PIL import Image
from docx import Document
from io import BytesIO

app = Flask(__name__)

# Configuración para Tesseract (asegúrate de que la ruta esté configurada correctamente)
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener la imagen cargada por el usuario
        imagen = request.files['imagen']
        
        # Guardar la imagen en el servidor
        imagen_path = os.path.join('uploads', imagen.filename)
        imagen.save(imagen_path)
        
        # Utilizar pytesseract para hacer OCR en la imagen
        texto_extraido = pytesseract.image_to_string(Image.open(imagen_path), lang='spa')
        
        # Crear un nuevo documento de Word y agregar el texto extraído
        documento = Document()
        documento.add_paragraph(texto_extraido)
        
        # Guardar el documento de Word en memoria
        output = BytesIO()
        documento.save(output)
        output.seek(0)
        
        # Eliminar la imagen cargada del servidor
        os.remove(imagen_path)
        
        # Descargar el documento de Word al navegador del usuario
        return send_file(output, as_attachment=True, download_name='manuscrito_convertido.docx')

    return render_template('inicio.html')

if __name__ == '__main__':
    app.run(debug=True)
