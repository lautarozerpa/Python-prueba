import PySimpleGUI as sg
import random

def Opciones(oficinas,lista_colores):
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
         sg.InputCombo(values=(oficinas), default_value=oficinas[0], size=(5, 1))],
        [sg.Text('6. Tipo de ayuda:'),
         sg.InputCombo(values=('Sin ayuda', 'Definiciones', 'Lista de palabras'), default_value='Sin ayuda',
                       size=(20, 1))],
        [sg.Ok(), sg.Cancel()]
    ]

    window = sg.Window('CONFIGURACION').Layout(layuot)

    bot, values = window.Read()

    return values

def Sopa(cant_sustantivos,cant_adjetivos,cant_verbos,color_sustantivos,color_adjetivos,color_verbos,orientacion,grafia,ayuda,palabras,temp):


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
        #elif verificar, ayuda(sg.window)

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

    # parametros a recibir
    palabras = ['carta', 'manta', 'caracol', 'pajaro','marioneta']
    oficinas = ['1', '2', '3'] #se debe recibir del archivo json
    temp = random.randint(10, 40)#oficina

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

    #funcion sopa
    Sopa(cant_sustantivos,cant_adjetivos,cant_verbos,color_sustantivos,color_adjetivos,color_verbos,orientacion,grafia,ayuda,palabras,temp)

if __name__ == '__main__':
    main()