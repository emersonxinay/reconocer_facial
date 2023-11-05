import pytesseract
from PIL import Image
from docx import Document

# Configura la ruta de Tesseract en tu sistema (ejemplo para Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ruta de la imagen del manuscrito que quieres escanear
imagen_path = 'ruta_de_la_imagen.png'

# Utiliza pytesseract para hacer OCR en la imagen
texto_extraido = pytesseract.image_to_string(Image.open(imagen_path), lang='spa')

# Crea un nuevo documento de Word y agrega el texto extraído
documento = Document()
documento.add_paragraph(texto_extraido)

# Guarda el documento de Word como un archivo .docx
documento.save('manuscrito_convertido.docx')

print('Manuscrito convertido y guardado como manuscrito_convertido.docx')
