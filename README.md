# para reconocer manuscritos y convertir a pdf y word 
## instalar dependencias para que funcione

```bash
brew install tesseract

```

## paquetes para instalar 

```bash
pip install pytesseract
pip install python-docx
```

## crear el entorno virtual y activarlo para instalar las dependencias de opencv:
```bash
pip install -r requirements.txt
```

primero ejecutar el archivo general para crear las imagenes y entrenar las imagenes 
```bash
python reconocimiento_general2.py
```
Segundo probar el reconocimiento facial con los datos entrenados 
```bash
python reconocimiento_despues_de_general2.py
```

