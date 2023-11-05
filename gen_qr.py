import pyqrcode
import png
from pyqrcode import QRCode

iniciando = 1234

# generamos codigo qr 
while iniciando <= 1239:
  roster = iniciando
  id = '65' + str(iniciando)
  # creamos los qr
  qr = pyqrcode.create(65 and id, error='L')
  # guardamos
  qr.png('A'+str(roster)+ '.png', scale=6)
  # y que sea incremental 
  iniciando = iniciando +1
  