import PySimpleGUI as sg
import random
from pattern.web import Wiktionary as wik
from pattern.es import verbs, tag, spelling, lexicon
import string
import json, os
import unicodedata


def elimina_tildes(cadena):
	s = ''.join((c for c in unicodedata.normalize('NFD', cadena) if unicodedata.category(c) != 'Mn'))
	return s


def limpiarOracion(Oracion):
	sinacentos = elimina_tildes(Oracion)
	sacareditar = sinacentos.replace("[editar]", "")
	sacarene = sacareditar.replace("\\n", "")
	sacaretimologia = sacarene.replace("Etimologia", "")
	return sacaretimologia


def BuscarEnWiki(palabra):
	engine = wik(language='es')
	# SELECCIONA LA PALABRA A BUSCAR
	article = engine.article(palabra)

	try:
		# BUSCA SI ES SUST,ADJ,VERB EN WIKI Y LO GUARDA EN tipowiki
		for section in article.sections:
			if ("SUSTANTIV") in (repr(section)).upper():
				tipowiki = "Sustantivo"
				break
			elif ("ADJETIV") in repr(section).upper():
				tipowiki = "Adjetivo"
				break
			elif ("VERB") in repr(section).upper():
				tipowiki = "Verbo"
				break

	# EXCEPCION POR SI NO ENCUENTRA LA PALABRA
	except (TypeError, AttributeError):
		tipowiki = ""
		print("La palabra no esta en Wiktionary")
	return tipowiki


def BuscarEnPattern(palabra):
	def clasificar(palabra):
		# if ("NN") in ( tag(palabra,tokenize=True, encoding='utf-8')):
		if ((tag(palabra, tokenize=True, encoding='utf-8')[0][1]) == "NN"):
			tipopattern = "Sustantivo"
		elif ((tag(palabra, tokenize=True, encoding='utf-8')[0][1]) == "JJ"):
			tipopattern = "Adjetivo"
		elif ((tag(palabra, tokenize=True, encoding='utf-8')[0][1]) == "VB"):
			tipopattern = "Verbo"
		else:
			tipopattern = ""
		return tipopattern

	if not palabra.lower() in verbs:
		if not palabra.lower() in spelling:
			if (not (palabra.lower() in lexicon) and not (palabra.upper() in lexicon) and not (
					palabra.capitalize() in lexicon)):
				print('La palabra no esta en pattern.es')
				tipopattern = ""
			else:
				tipopattern = clasificar(palabra)
		else:
			tipopattern = clasificar(palabra)
	else:
		tipopattern = clasificar(palabra)

	print()
	return tipopattern


def BuscarDefinicionEnWiki(palabra):
	contenido = ""
	engine = wik(language='es')
	article = engine.article(palabra)
	for section in article.sections:
		if ("Etimolog") in repr(section):
			contenido = (repr(section.content))
	return limpiarOracion(contenido)


def GuardarDatos(palabra, tipo, definicion):
	datonuevo = {}
	datonuevo.setdefault("Palabra", palabra)
	datonuevo.setdefault("Tipo", tipo)
	datonuevo.setdefault("Definicion", definicion)
	if os.path.isfile("Palabras.json"):
		with open("Palabras.json", mode='r') as f:
			data = json.loads(f.read())
		f.close()
		data.append(datonuevo)
		with open("Palabras.json", 'w') as f:
			json.dump(data, f, indent=4)
	else:
		data = [datonuevo]
		with open("Palabras.json", "w")as f:
			json.dump(data, f, indent=4)


def ReportePatternTipo(palabra, tipo):
	Log = "La palabra " + palabra + " no se encuentra en pattern como un " + tipo
	f = open('LogPattern.txt', 'a')
	f.write('\n' + Log)
	f.close()


def ReportePatternYWiki(palabra):
	Log = "La palabra " + palabra + " no se encuentra en pattern ni en wiktionary"
	f = open('LogPatternYWiki.txt', 'a')
	f.write('\n' + Log)
	f.close()


def main_comprobacion_palabra(palabra):
	tipoWiki = BuscarEnWiki(palabra.lower())
	tipoPattern = BuscarEnPattern(palabra)
	if (tipoWiki != ""):
		if (tipoPattern != ""):
			# Si wiki y pattern son iguales, se guarda
			if (tipoWiki == tipoPattern):
				definicion = BuscarDefinicionEnWiki(palabra.lower())
				GuardarDatos(palabra, tipoWiki, definicion)
			# Si wiki y pattern son distintas, se toma la de wiki y se hace reporte en pattern
			else:
				definicion = BuscarDefinicionEnWiki(palabra.lower())
				GuardarDatos(palabra, tipoWiki, definicion)
				ReportePatternTipo(palabra, tipoWiki)
		else:
			definicion = BuscarDefinicionEnWiki(palabra.lower())
			GuardarDatos(palabra, tipoWiki, definicion)
			ReportePatternTipo(palabra, tipoWiki)
	elif (
			tipoPattern != ""):  # Si no esta en wiki pero si esta en pattern se pide la definicion al profesor y se guarda
		definicion = input(print("Ingrese definicion de la palabra"))
		GuardarDatos(palabra, tipoPattern, definicion)
	else:
		ReportePatternYWiki(palabra)


def buscar_oficinas():
	arc = open('datos-oficinas.json', 'r')
	data = json.load(arc)
	lista = []
	for x in data:
		lista.append(x)
	arc.close()
	return lista


def calcular_promedio(ofi):
	arc = open('datos-oficinas.json', 'r')
	data = json.load(arc)
	data = data[ofi]
	suma = 0
	cant_sumas = 0
	for elem in data:
		cant_sumas = cant_sumas + 1
		suma = suma + elem['temp']
	return suma / cant_sumas


def Opciones(oficinas, lista_colores):
	layuot = [
		[sg.Text('OPCIONES')],
		[sg.Frame('1. Cantidad de palabras', layout=[
			[sg.Text('Numero de sustantivos:'),
			 sg.InputCombo(values=('0', '1', '2', '3', '4', '5'), default_value='1', size=(5, 1))],
			[sg.Text('Numero de adjetivos:'),
			 sg.InputCombo(values=('0', '1', '2', '3', '4', '5'), default_value='1', size=(5, 1))],
			[sg.Text('Numero de verbos:'),
			 sg.InputCombo(values=('0', '1', '2', '3', '4', '5'), default_value='1', size=(5, 1))]],
				  relief=sg.RELIEF_GROOVE)],
		[sg.Frame('2. Color de palabras', layout=[
			[sg.Text('Color de sustantivos:'),
			 sg.InputCombo(values=(lista_colores), default_value=lista_colores[0], size=(20, 1))],
			[sg.Text('Color de adjetivos:'),
			 sg.InputCombo(values=(lista_colores), default_value=lista_colores[1], size=(20, 1))],
			[sg.Text('Color de verbos:'),
			 sg.InputCombo(values=(lista_colores), default_value=lista_colores[2], size=(20, 1))]],
				  relief=sg.RELIEF_GROOVE)],
		[sg.Text('3. Orientacion:'),
		 sg.InputCombo(values=('Horizontal', 'Vertical'), default_value='Horizontal', size=(20, 1))],
		[sg.Text('4. Tipo de letra:'),
		 sg.InputCombo(values=('Mayuscula', 'Minuscula'), default_value='Mayuscula', size=(20, 1))],
		[sg.Text('5. Oficina para tomar datos:'),
		 sg.InputCombo(values=(oficinas), default_value=oficinas[0], size=(20, 1))],
		[sg.Text('6. Tipo de ayuda:'),
		 sg.InputCombo(values=('Sin ayuda', 'Definiciones', 'Lista de palabras'), default_value='Sin ayuda',
					   size=(20, 1))],
		[sg.Ok(), sg.Cancel()]
	]

	window = sg.Window('CONFIGURACION').Layout(layuot)

	bot, values = window.Read()
	window.Close()
	return values,bot


def agregar_eliminar():
	layout = [
		[sg.Text('7. Opcion para agregar o borrar palabras: '), sg.Input(default_text='ingrese una palabra'),
		 sg.Button('Agregar'), sg.Button('Eliminar')],
		[sg.Button('Terminar')]
	]

	window = sg.Window('CONFIGURACION DE PALABRAS', ).Layout(layout)

	while True:
		button, values = window.Read()
		if button is not 'Terminar':
			if button == 'Agregar':
				main_comprobacion_palabra(values[0])
			else:
				if os.path.isfile("Palabras.json"):
					arc = open('Palabras.json', 'r')
					data = json.load(arc)
					arc.close()
					for i in range(len(data)):
						if values[0] == data[i]['palabra']:
							data.remove(data[i])
							arc = open('Palabras.json', 'w')
							json.dump(data, arc)
							arc.close()
			sg.Popup('operacion finalizada')
		else:
			window.Close()
			break


def obtenerListaPalabras(cant_sustantivos, cant_adjetivos, cant_verbos):
	palabras = []
	ListaSustantivos = []
	ListaAdjetivos = []
	ListaVerbos = []
	with open("Palabras.json") as file:
		data = json.load(file)
		for d in data:
			if (d["Tipo"] == "Sustantivo"):
				ListaSustantivos.append(d["Palabra"])
			elif (d["Tipo"] == "Adjetivo"):
				ListaAdjetivos.append(d["Palabra"])
			elif (d["Tipo"] == "Verbo"):
				ListaVerbos.append(d["Palabra"])

	#Actualizar cantidad de palabras
	if (cant_sustantivos > len(ListaSustantivos)):
		cant_sustantivos = len(ListaSustantivos)
	if (cant_adjetivos > len(ListaAdjetivos)):
		cant_adjetivos = len(ListaAdjetivos)
	if (cant_verbos > len(ListaVerbos)):
		cant_verbos = len(ListaVerbos)

	#Tomar palabras
	ListaS = []
	ListaA = []
	ListaV = []
	for l in range(cant_sustantivos):
		pal=random.choice(ListaSustantivos)
		ListaS.append(pal)
		ListaSustantivos.remove(pal)
	for l in range(cant_adjetivos):
		pal=random.choice(ListaAdjetivos)
		ListaA.append(pal)
		ListaAdjetivos.remove(pal)
	for l in range(cant_verbos):
		pal=random.choice(ListaVerbos)
		ListaV.append(pal)
		ListaVerbos.remove(pal)

	for l in ListaS:
		ListaSustantivos.append(l)
	for l in ListaA:
		ListaAdjetivos.append(l)
	for l in ListaV:
		ListaVerbos.append(l)

	#Entrelazar palabras
	for k in range(cant_verbos+cant_adjetivos+cant_sustantivos):
		num=random.randint(0,2)
		if num == 0 and ListaS:
			pal = random.choice(ListaS)
			palabras.append(pal)
			ListaS.remove(pal)
		else:
			num=random.randint(1,2)
		if num == 1 and ListaA:
			pal = random.choice(ListaA)
			palabras.append(pal)
			ListaA.remove(pal)
		else:
			num = 2
		if num == 2 and ListaV:
			pal = random.choice(ListaV)
			palabras.append(pal)
			ListaV.remove(pal)
		else:
			if ListaS:
				pal = random.choice(ListaS)
				palabras.append(pal)
				ListaS.remove(pal)
			else:
				if ListaA:
					pal = random.choice(ListaA)
					palabras.append(pal)
					ListaA.remove(pal)
	return palabras, ListaSustantivos, ListaAdjetivos, ListaVerbos, str(cant_sustantivos), str(cant_adjetivos), str(cant_verbos)


def CrearListaDefiniciones(lista):
	ListaDefiniciones = []
	with open("Palabras.json") as file:
		data = json.load(file)
		for d in data:
			if (d["Palabra"]) in lista:
				ListaDefiniciones.append(d["Definicion"])
	return (ListaDefiniciones)


def AbrirVentanaAyuda(ListaDefiniciones, color_de_fondo):
	x = 0
	while True:
		layoutAyuda = [[sg.Text(ListaDefiniciones[x], background_color=(color_de_fondo[0]), size=(30, 30))],
					   [sg.Button('< Prev'), sg.Button('Next >'), sg.Button('Volver')]]
		if x == 0:
			layoutAyuda[1].pop(0)
		elif x == (len(ListaDefiniciones) - 1):
			layoutAyuda[1].pop(1)
		winAyuda = sg.Window('Ayuda', background_color=color_de_fondo[1]).Layout(layoutAyuda)
		event2, values2 = winAyuda.Read()
		if event2 == ('Volver'):
			winAyuda.Close()
			break
		elif (event2 == '< Prev') and (x >= 0):
			x = x - 1
			winAyuda.Close()
		elif (event2 == 'Next >') and (x < (len(ListaDefiniciones) - 1)):
			x = x + 1
		winAyuda.Close()


def AbrirVentanaAyudaSimple(Ayuda, color_de_fondo):
	layoutAyuda = [[sg.Text(Ayuda, background_color=(color_de_fondo[0]), size=(30, 30))], [sg.Button('Volver')]]
	winAyuda = sg.Window('Ayuda', background_color=color_de_fondo[1]).Layout(layoutAyuda)
	e, v = winAyuda.Read()
	if e is 'Volver':
		winAyuda.Close()


def colorear_matriz(mc,matriz, sustantivos, adjetivos, verbos, lineas, colorS, colorA, colorV, orientacion):
	for a in range(2):
		sustantivos.append('relleno')
		adjetivos.append('relleno')
		verbos.append('relleno')
	for i in range(len(lineas)):
		x = 0
		palabra_sin_encontrar = True
		while palabra_sin_encontrar:
			if x < len(sustantivos):
				if sustantivos[x].upper() in lineas[i].upper():
					palabra_sin_encontrar = False
					color = colorS
					pal = sustantivos[x]
			if x < len(adjetivos):
				if adjetivos[x].upper() in lineas[i].upper():
					palabra_sin_encontrar = False
					color = colorA
					pal = adjetivos[x]
			if x < len(verbos):
				if verbos[x].upper() in lineas[i].upper():
					palabra_sin_encontrar = False
					color = colorV
					pal = verbos[x]
			x=x+1
		x = 0
		if orientacion == 'Horizontal':
			while matriz[i][x]['letra'].upper() != pal[0].upper():
				x = x + 1
			for k in range(x, x + len(pal)):
				mc[i][k]['color'] = color
		else:
			while matriz[x][i]['letra'].upper() != pal[0].upper():
				x = x + 1
			for k in range(x, x + len(pal)):
				mc[k][i]['color'] = color


def Verificacion(matriz, matriz_correcta, ancho, alto,orientacion):
	if orientacion == 'Horizontal':
		for x in range(alto):
			for y in range(ancho):
				if matriz[x][y]['color'] == matriz_correcta[x][y]['color']:
					matriz[x][y]['color'] = 'green'
				else:
					matriz[x][y]['color'] = 'red'
	else:
		for x in range(ancho):
			for y in range(alto):
				if matriz[x][y]['color'] == matriz_correcta[x][y]['color']:
					matriz[x][y]['color'] = 'green'
				else:
					matriz[x][y]['color'] = 'red'
	return matriz


def Dibujar_sopa_final(matriz, color_de_fondo, orientacion, ancho, alto, BOX_SIZE):
	if orientacion == 'Horizontal':

		# Layout
		layout = [
			[sg.Text('', key='_OUTPUT_')],
			[sg.Graph((ancho * 40 - 1, alto * 40 - 1), (0, alto * 25 - 1), (ancho * 25, 0 - 1), key='_GRAPH_',
					  background_color=color_de_fondo[0], change_submits=True, drag_submits=False)],
			[sg.Button('Salir')]
		]

		window = sg.Window('Sopa de letras', background_color=color_de_fondo[1]).Layout(layout).Finalize()

		g = window.FindElement('_GRAPH_')

		# Dibujo horizontal
		for row in range(alto):
			for col in range(ancho):
				letra = matriz[row][col]['letra']
				color_actual = matriz[row][col]['color']
				g.DrawRectangle((col * BOX_SIZE, row * BOX_SIZE),
								(col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE),
								line_color='black', fill_color=color_actual)

				g.DrawText('{}'.format(letra), (col * BOX_SIZE + 13, row * BOX_SIZE + 13), font='Courier 25')


	else:

		# Layout
		layout = [
			[sg.Text('', key='_OUTPUT_')],
			[sg.Graph((alto * 40 - 1, ancho * 40 - 1), (0, ancho * 25 - 1), (alto * 25, 0 - 1), key='_GRAPH_',
					  background_color=color_de_fondo[0], change_submits=True, drag_submits=False)],
			[sg.Button('Salir')]
		]

		window = sg.Window('Sopa de letras', background_color=color_de_fondo[1]).Layout(layout).Finalize()

		g = window.FindElement('_GRAPH_')

		# Dibujo vertical
		for row in range(ancho):
			for col in range(alto):
				letra = matriz[row][col]['letra']
				color_actual = matriz[row][col]['color']
				g.DrawRectangle((col * BOX_SIZE, row * BOX_SIZE),
								(col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE),
								fill_color=color_actual, line_color='black', )

				g.DrawText('{}'.format(letra), (col * BOX_SIZE + 13, row * BOX_SIZE + 13), font='Courier 25')

	e,v=window.Read()

	if e == 'Salir':
		window.Close()


def Sopa(cant_sustantivos, cant_adjetivos, cant_verbos, color_sustantivos, color_adjetivos, color_verbos, orientacion,
		 grafia, ayuda, palabras, sustantivos, adjetivos, verbos, temp):

	lista_palabras = palabras.copy()

	ListaDefiniciones = CrearListaDefiniciones(lista_palabras)
	# parametros locales
	alto = len(palabras)
	ancho = (max(len(pal) for pal in palabras) + 3)
	BOX_SIZE = 25
	matriz = []
	matriz_correcta= []


	# Calculo de temperatura
	if temp > 30:
		color_de_fondo = ['pink', 'red']
	else:
		color_de_fondo = ['lightblue', 'blue']

	color_actual = color_de_fondo[1]


	# Relleno de palabras
	for i in range(len(palabras)):
		pal = palabras[i]
		while (len(pal) < ancho):
			op = random.randint(0, 1)
			if op == 1:
				l = random.choice('qwertyuioplkjhgfdsazxcvbnm')
				while l == lista_palabras[i][0]:
					l = random.choice('qwertyuioplkjhgfdsazxcvbnm')
				pal = pal + l
			else:
				l = random.choice('qwertyuioplkjhgfdsazxcvbnm')
				while l == lista_palabras[i][0]:
					l = random.choice('qwertyuioplkjhgfdsazxcvbnm')
				pal = l + pal
		palabras[i] = pal

	# Calculo de grafia
	if grafia == 'Mayuscula':
		for i in range(len(palabras)):
			palabras[i] = palabras[i].upper()
	else:
		for i in range(len(palabras)):
			palabras[i] = palabras[i].lower()

	# Calculo de orientacion

	if orientacion == 'Horizontal':

		# Layout
		layout = [
			[sg.Text('temperatura actual: ' + str(temp)), sg.Text('', key='_OUTPUT_')],
			[sg.Graph((ancho * 40 - 1, alto * 40 - 1), (0, alto * 25 - 1), (ancho * 25, 0 - 1), key='_GRAPH_',
					  background_color=color_de_fondo[0], change_submits=True, drag_submits=False)],
			[sg.Button('Sustantivo'), sg.Button('Adjetivo'), sg.Button('Verbo'), sg.Button('Verificar'),
			 sg.Button('Ayuda'), sg.Button('Salir')]
		]

		window = sg.Window('Sopa de letras', background_color=color_de_fondo[1]).Layout(layout).Finalize()

		g = window.FindElement('_GRAPH_')

		# Dibujo horizontal
		for row in range(alto):
			matriz.append([])
			matriz_correcta.append([])
			for col in range(ancho):
				letra = palabras[row][col]
				g.DrawRectangle((col * BOX_SIZE, row * BOX_SIZE),
								(col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE),
								line_color='black')

				g.DrawText('{}'.format(letra), (col * BOX_SIZE + 13, row * BOX_SIZE + 13), font='Courier 25')
				dic_casillero = {'letra': letra, 'color': color_actual}
				d = {'letra': letra, 'color': color_actual}
				matriz[row].append(dic_casillero)
				matriz_correcta[row].append(d)

	else:

		# Layout
		layout = [
			[sg.Text('temperatura actual: ' + str(temp)), sg.Text('', key='_OUTPUT_')],
			[sg.Graph((alto * 40 - 1, ancho * 40 - 1), (0, ancho * 25 - 1), (alto * 25, 0 - 1), key='_GRAPH_',
					  background_color=color_de_fondo[0], change_submits=True, drag_submits=False)],
			[sg.Button('Sustantivo'), sg.Button('Adjetivo'), sg.Button('Verbo'), sg.Button('Verificar'),
			 sg.Button('Ayuda'), sg.Button('Salir')]
		]

		window = sg.Window('Sopa de letras', background_color=color_de_fondo[1]).Layout(layout).Finalize()

		g = window.FindElement('_GRAPH_')

		# Dibujo vertical
		for row in range(ancho):
			matriz.append([])
			matriz_correcta.append([])
			for col in range(alto):
				letra = palabras[col][row]
				g.DrawRectangle((col * BOX_SIZE, row * BOX_SIZE),
								(col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE),
								line_color='black')

				g.DrawText('{}'.format(letra), (col * BOX_SIZE + 13, row * BOX_SIZE + 13), font='Courier 25')
				dic_casillero = {'letra': letra, 'color': color_actual}
				d = {'letra': letra, 'color': color_actual}
				matriz[row].append(dic_casillero)
				matriz_correcta[row].append(d)


	color_actual= color_de_fondo[0]
	ant=color_actual

	# Uso de la sopa
	while True:  # Event Loop
		event, values = window.Read()
		print(event, values)
		if event is None or event == 'Salir':
			break
		elif event is 'Sustantivo':
			color_actual = color_sustantivos
		elif event is 'Adjetivo':
			color_actual = color_adjetivos
		elif event is 'Verbo':
			color_actual = color_verbos
		elif event is 'Ayuda':
			if ayuda == 'Definiciones':
				winayuda_active = True
				window.Hide()
				AbrirVentanaAyuda(ListaDefiniciones, color_de_fondo)
				window.UnHide()
			elif ayuda == 'Lista de palabras':
				winayuda_active = True
				window.Hide()
				AbrirVentanaAyudaSimple(lista_palabras, color_de_fondo)
				window.UnHide()
			else:
				winayuda_active = True
				window.Hide()
				AbrirVentanaAyudaSimple(
					'sustantivos: ' + cant_sustantivos + ' adjetivos: ' + cant_adjetivos + ' verbos: ' + cant_verbos,
					color_de_fondo)
				window.UnHide()
		elif event is 'Verificar':
			colorear_matriz(matriz_correcta,matriz, sustantivos, adjetivos, verbos, palabras, color_sustantivos,
							color_adjetivos,color_verbos, orientacion)
			matriz_resultante = Verificacion(matriz, matriz_correcta, ancho, alto,orientacion)
			Dibujar_sopa_final(matriz_resultante, color_de_fondo, orientacion, ancho, alto, BOX_SIZE)
			break

		mouse = values['_GRAPH_']
		cambio= False

		if event == '_GRAPH_':
			if mouse == (None, None):
				continue
			box_x = mouse[0] // BOX_SIZE
			box_y = mouse[1] // BOX_SIZE
			letter_location = (box_x * BOX_SIZE + 13, box_y * BOX_SIZE + 13)
			cambio = False
			if orientacion == 'Horizontal':
				if (box_x < ancho and box_y < alto):
					if matriz[box_y][box_x]['color'] == color_actual:
						ant= color_actual
						color_actual = color_de_fondo[0]
						cambio=True
					matriz[box_y][box_x]['color'] = color_actual
					g.DrawRectangle((box_x * BOX_SIZE, box_y * BOX_SIZE),
									(box_x * BOX_SIZE + BOX_SIZE, box_y * BOX_SIZE + BOX_SIZE), line_color='black',
									fill_color=color_actual)
					g.DrawText('{}'.format(matriz[box_y][box_x]['letra']), letter_location, font='Courier 25')
					if cambio:
						color_actual= ant
			else:
				if (box_x < alto and box_y < ancho):
					if (matriz[box_y][box_x]['color'] == color_actual):
						ant= color_actual
						color_actual = color_de_fondo[0]
						cambio= True
					matriz[box_y][box_x]['color'] = color_actual
					g.DrawRectangle((box_x * BOX_SIZE, box_y * BOX_SIZE),
									(box_x * BOX_SIZE + BOX_SIZE, box_y * BOX_SIZE + BOX_SIZE), line_color='black',
									fill_color=color_actual)
					g.DrawText('{}'.format(matriz[box_y][box_x]['letra']), letter_location, font='Courier 25')
					if cambio:
						color_actual= ant

	window.Close()


def main():
	# Generacion de oficinas disponibles:
	oficinas = buscar_oficinas()

	# Generacion de colores
	colores = {'amarillo': 'yellow', 'gris': 'grey', 'marron': 'brown', 'naranja': 'orange', 'verde': 'green',
			   'violeta': 'purple'}
	lista_colores = []
	for color in colores:
		lista_colores.append(color)

	# funcion para configuracion
	values, bot = Opciones(oficinas, lista_colores)
	if bot is 'Ok':
		cant_sustantivos = values[0]
		cant_adjetivos = values[1]
		cant_verbos = values[2]
		color_sustantivos = colores[values[3]]
		color_adjetivos = colores[values[4]]
		color_verbos = colores[values[5]]
		orientacion = values[6]
		grafia = values[7]
		oficina = values[8]
		ayuda = values[9]

		# Generacion de temperatura promedio
		temp = calcular_promedio(oficina)

		# Funcion para agregar o eliminar palabras
		agregar_eliminar()

		# Generacion de lista de palabras
		datos = obtenerListaPalabras(int(cant_sustantivos), int(cant_adjetivos), int(cant_verbos))
		palabras = datos[0]
		ListaSustantivos = datos[1]
		ListaAdjetivos = datos[2]
		ListaVerbos = datos[3]
		cant_sustantivos=datos[4]
		cant_adjetivos=datos[5]
		cant_verbos=datos[6]

		# funcion sopa
		Sopa(cant_sustantivos, cant_adjetivos, cant_verbos, color_sustantivos, color_adjetivos, color_verbos, orientacion,
			 grafia, ayuda, palabras, ListaSustantivos, ListaAdjetivos, ListaVerbos, temp)


if __name__ == '__main__':
	main()
