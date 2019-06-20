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
	contenido=""
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
    data= json.load(arc)
    lista=[]
    for x in data:
        lista.append(x)
    arc.close()
    return lista


def calcular_promedio(ofi):
    arc = open('datos-oficinas.json', 'r')
    data = json.load(arc)
    data= data[ofi]
    suma=0
    cant_sumas=0
    for elem in data:
        cant_sumas= cant_sumas +1
        suma = suma + elem['temp']
    return suma/cant_sumas



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

    return values


def agregar_eliminar():
    layout=[
        [sg.Text('7. Opcion para agregar o borrar palabras: '),sg.Input(default_text='ingrese una palabra'),sg.Button('Agregar'),sg.Button('Eliminar')],
        [sg.Button('Terminar')]
    ]

    window= sg.Window('CONFIGURACION DE PALABRAS',).Layout(layout)

    while True:
        button, values= window.Read()
        if button is not 'Terminar':
            if button == 'Agregar':
                main_comprobacion_palabra(values[0])
            else:
                if os.path.isfile("Palabras.json"):
                    arc= open('Palabras.json','r')
                    data= json.load(arc)
                    arc.close()
                    for i in range(len(data)):
                        if values[0] == data[i]['palabra']:
                            data.remove(data[i])
                            arc= open('Palabras.json','w')
                            json.dump(data,arc)
                            arc.close()
            sg.Popup('operacion finalizada')
        else:
            break


def obtenerListaPalabras(cant_sustantivos,cant_adjetivos,cant_verbos):
    palabras=[]
    ListaSustantivos=[]
    ListaAdjetivos=[]
    ListaVerbos=[]
    with open("Palabras.json") as file:
        data=json.load(file)
        for d in data:
            if(d["Tipo"]== "Sustantivo"):
                ListaSustantivos.append(d["Palabra"])
            elif(d["Tipo"]=="Adjetivo"):
                ListaAdjetivos.append(d["Palabra"])
            else:
                ListaVerbos.append(d["Palabra"])
    ListaS=ListaSustantivos.copy()
    ListaA=ListaAdjetivos.copy()
    ListaV=ListaVerbos.copy()
    for i in range(cant_sustantivos):
        if(ListaS):
            pal=random.choice(ListaS)
            palabras.append(pal)
            ListaS.remove(pal)
        else:
            break
    for i in range(cant_adjetivos):
        if(ListaA):
            pal=random.choice(ListaA)
            palabras.append(pal)
            ListaA.remove(pal)
        else:
            for i in range(cant_verbos):
                if(ListaV):
                    pal=random.choice(ListaV)
                    palabras.append(pal)
                    ListaV.remove(pal)
                else:
                    break
    return palabras,ListaSustantivos,ListaAdjetivos,ListaVerbos

def CrearListaDefiniciones(lista):
	ListaDefiniciones=[]
	with open("Palabras.json") as file:
		data=json.load(file)
		for d in data:
			if(d["Palabra"]) in lista:
				ListaDefiniciones.append(d["Definicion"])
	return(ListaDefiniciones)
				
			
	

def Sopa(cant_sustantivos,cant_adjetivos,cant_verbos,color_sustantivos,color_adjetivos,color_verbos,orientacion,grafia,ayuda,palabras,temp):

    lista_palabras=palabras.copy()
    
    ListaDefiniciones=CrearListaDefiniciones(lista_palabras)

    # parametros locales
    alto = len(palabras)
    ancho = max(len(pal) for pal in palabras)
    BOX_SIZE = 25
    matriz = []



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
                pal = pal + random.choice('qwertyuioplkjhgfdsazxcvbnm')
            else:
                pal = random.choice('qwertyuioplkjhgfdsazxcvbnm') + pal
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

        #Layout
        layout = [
            [sg.Text('temperatura actual: ' + str(temp)), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((ancho * 40 - 1, alto * 40 - 1), (0, alto * 25 - 1), (ancho * 25, 0 - 1), key='_GRAPH_',
                      background_color=color_de_fondo[0], change_submits=True, drag_submits=False)],
            [sg.Button('Sustantivo'), sg.Button('Adjetivo'), sg.Button('Verbo'),sg.Button('Verificar'),sg.Button('Ayuda'), sg.Button('Salir')]
        ]

        window = sg.Window('Sopa de letras', background_color=color_de_fondo[1]).Layout(layout).Finalize()

        g = window.FindElement('_GRAPH_')

        #Dibujo
        for row in range(alto):
            matriz.append([])
            for col in range(ancho):
                letra = palabras[row][col]
                g.DrawRectangle((col * BOX_SIZE, row * BOX_SIZE), (col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE),
                                line_color='black')

                g.DrawText('{}'.format(letra), (col * BOX_SIZE + 13, row * BOX_SIZE + 13), font='Courier 25')
                matriz[row].append(letra)
    else:

        #Layout
        layout = [
            [sg.Text('temperatura actual: ' + str(temp)), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((alto * 40 - 1, ancho * 40 - 1), (0, ancho * 25 - 1), (alto * 25, 0 - 1), key='_GRAPH_',
                      background_color=color_de_fondo[0], change_submits=True, drag_submits=False)],
            [sg.Button('Sustantivo'), sg.Button('Adjetivo'), sg.Button('Verbo'),sg.Button('Verificar'),sg.Button('Ayuda'),sg.Button('Salir')]
        ]

        window = sg.Window('Sopa de letras', background_color=color_de_fondo[1]).Layout(layout).Finalize()

        g = window.FindElement('_GRAPH_')


        #Dibujo
        for row in range(ancho):
            matriz.append([])
            for col in range(alto):
                letra = palabras[col][row]
                g.DrawRectangle((col * BOX_SIZE, row * BOX_SIZE), (col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE),
                                line_color='black')

                g.DrawText('{}'.format(letra), (col * BOX_SIZE + 13, row * BOX_SIZE + 13), font='Courier 25')
                matriz[row].append(letra)

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
                window= sg.Window('Definiciones', background_color=color_de_fondo[0]).Layout([[sg.Text('')]])
            elif ayuda == 'Lista de palabras':
                window= sg.Window('Lista de palabras', background_color=color_de_fondo[0]).Layout([[sg.Text(lista_palabras)]])
                window.Read()
            else:
                window= sg.Window('Cantidad de palabras', background_color=color_de_fondo[0]).Layout([[sg.Text('sustantivos: ' + cant_sustantivos + ' adjetivos: ' + cant_adjetivos + ' verbos: ' + cant_verbos)]])
                window.Read()
        elif event is 'Verificar':
            print('Modulo sin hacer')

        mouse = values['_GRAPH_']

        if event == '_GRAPH_':
            if mouse == (None, None):
                continue
            box_x = mouse[0] // BOX_SIZE
            box_y = mouse[1] // BOX_SIZE
            letter_location = (box_x * BOX_SIZE + 13, box_y * BOX_SIZE + 13)
            if orientacion== 'Horizontal':
                if (box_x < ancho and box_y < alto):
                    print(box_x, box_y)
                    g.DrawRectangle((box_x * BOX_SIZE, box_y * BOX_SIZE),
                                    (box_x * BOX_SIZE + BOX_SIZE, box_y * BOX_SIZE + BOX_SIZE), line_color='black',
                                    fill_color=color_actual)
                    g.DrawText('{}'.format(matriz[box_y][box_x]), letter_location, font='Courier 25')
            else:
                if (box_x < alto and box_y < ancho):
                    g.DrawRectangle((box_x * BOX_SIZE, box_y * BOX_SIZE),
                                    (box_x * BOX_SIZE + BOX_SIZE, box_y * BOX_SIZE + BOX_SIZE), line_color='black',
                                    fill_color=color_actual)
                    g.DrawText('{}'.format(matriz[box_y][box_x]), letter_location, font='Courier 25')

    window.Close()

def main():

    #Generacion de oficinas disponibles:
    oficinas= buscar_oficinas()


    #Generacion de colores
    colores = {'amarillo': 'yellow', 'azul': 'blue', 'gris': 'grey', 'rojo': 'red', 'verde': 'green',
               'violeta': 'meduimorchid'}
    lista_colores = []
    for color in colores:
        lista_colores.append(color)

    #funcion para configuracion
    values= Opciones(oficinas,lista_colores)
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


    #Generacion de temperatura promedio
    temp = calcular_promedio(oficina)

    #Funcion para agregar o eliminar palabras
    agregar_eliminar()

    #Generacion de lista de palabras
    datos=obtenerListaPalabras(int(cant_sustantivos),int(cant_adjetivos),int(cant_verbos))
    palabras=datos[0]
    ListaSustantivos= datos[1]
    ListaAdjetivos=datos[2]
    ListaVerbos=datos[3]

    #funcion sopa
    Sopa(cant_sustantivos,cant_adjetivos,cant_verbos,color_sustantivos,color_adjetivos,color_verbos,orientacion,grafia,ayuda,palabras,temp)

if __name__ == '__main__':
    main()
