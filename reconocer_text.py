import pytesseract
from PIL import Image

# Ruta de la imagen del manuscrito que quieres escanear
imagen_path = './saludo.jpeg'

# Utiliza pytesseract para hacer OCR en la imagen
texto_extraido = pytesseract.image_to_string(Image.open(imagen_path), lang='spa')

print('Texto extraído:', texto_extraido)
