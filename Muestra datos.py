from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import Adafruit_DHT

class Temperatura:
	def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
		self._sensor = sensor
		self._data_pin = pin
		
	def datos_sensor(self):
		humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
		return {'temperatura': temperatura, 'humedad': humedad}

class Matriz:
	def __init__(self, numero_matrices=1, orientacion=0, rotacion=0, ancho=8, alto=8):
		self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
		self.serial = spi(port=0, device=0, gpio=noop())
		self.device = max7219(self.serial, width=ancho, height= alto, cascaded=numero_matrices, rotate=rotacion)
	def mostrar_mensaje(self, msg, delay=0.1, font=1):
		show_message(self.device, msg, fill="white", font=proportional(self.font[font]), scroll_delay=delay)

def main():
	temp = Temperatura()
	datos=temp.datos_sensor()
	matriz = Matriz(numero_matrices=2, ancho=16)
	mensaje=datos['temperatura'] + ' ' + datos['humedad'] + ' '
	matriz.mostrar_mensaje(mensaje, delay=0.3)
	serial = spi(port=0, device=0, gpio=noop())
	device = max7219(serial, width, height, cascaded, rotate)
	show_message(device, msg, font,)max7219(serial, width, height, cascaded, rotate)

if __name__ == '__main__':
	main()
