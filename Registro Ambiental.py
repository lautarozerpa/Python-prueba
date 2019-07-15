import json, os
import time
import Adafruit_DHT
class Temperatura:
	def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
		self._sensor = sensor
		self._data_pin = pin
		
	def datos_sensor(self):
		humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
		return {'temperatura': temperatura, 'humedad': humedad}

def GuardarDatosSensor(datos, oficina):
	if os.path.isfile("datos-oficinas.json"):
			with open("datos-oficinas.json", mode='r') as f:
				data = json.loads(f.read())
			f.close()
			if(oficina in data):
				datoviejo=data[oficina]
				data.setdefault(oficina, datoviejo.append(datos))
			else:
				listanueva=[datos]
				data.setdefault(oficina,listanueva)
			with open("datos-oficinas.json", 'w') as f:
				json.dump(data, f, sort_keys=True, indent=4)
	else:
		data = {}
		data[oficina]=[datos]
		with open("datos-oficinas.json", "w")as f:
			json.dump(data, f, sort_keys=True, indent=4)
def main():
	temp = Temperatura()
	fecha=time.strftime("%a %d %b, %y ")
	oficina= "oficina" + input("ingrese numero de oficina: ")
	while True:
		datostemp=temp.datos_sensor()
		datos= {'temp':datostemp['temperatura'], 'humedad':datostemp['humedad'],'fecha':fecha}
		GuardarDatosSensor(datos, oficina)
		time.sleep(60)

if __name__ == '__main__':
	main()
