import pygame
from graficos import config
from .texto import *
from graficos import config
from . import grafica

def crear_grilla(matriz: list, ventana: any, celda: int = 25, spacing: int = 27)-> dict:

    '''
    Crea una grilla centrada e interactiva mediante pygame

    Arg: recibe matriz -> para hacer calculos internos
            ventana -> para tener donde imprimirla
            celda -> se puede cambiar el tamano de celda (por default 25 pix.)
            spacing -> por lo general es el tamano de celda + pix. de espacio entre las mismas.
                            (por default 27)

    Return: Retorna una grilla
    '''

    grilla = []
    
    alto_total = len(matriz) * spacing
    ancho_total = len(matriz[0]) * spacing

    ventana_ancho, ventana_alto = ventana.get_size()

    y_base = (ventana_alto - alto_total) // 2
    x_base = (ventana_ancho - ancho_total) // 2


    for i in range(len(matriz)):
        y = y_base + i * spacing
        fila = []
        for j in range(len(matriz[i])):

            x = x_base + j * spacing

            surface = pygame.Surface((celda, celda))
            surface.fill((255, 255, 255))

            rect = surface.get_rect(topleft=(x, y))

            fila.append({
                "surface": surface,
                "rect": rect,
                "color": config.BLANCO,
                "valor": 0 #equivalencia en 0  y 3
            })           
        grilla.append(fila)

    return grilla, x_base, y_base

def calcular_pistas(lista: list) -> list:
    '''
    Calcula las pistas por fila, de una lista.
 
    Arg: lista -> para recorrer y calcular.

    Return: pistas en lista.
    '''

    pistas = []
    contador = 0

    for i in range(len(lista)):
        if lista[i] == 1:
            contador += 1
        elif lista[i] == 0 and contador != 0:
            pistas.append(contador)
            contador = 0

    if contador > 0:
        pistas.append(contador)
        contador = 0
    
    return pistas

def calcular_pistas_v2(matriz: list, columna: int) -> list:
    '''
    Calcula las pistas por columna, de una matriz.
 
    Arg: lista -> para recorrer y calcular.
        columna -> indice columna

    Return: pistas en lista.
    '''

    pistas = []
    contador = 0

    for i in range(len(matriz)):
        if matriz[i][columna] == 1:
                contador += 1
        elif matriz[i][columna] == 0 and contador != 0:
            pistas.append(contador)
            contador = 0

    if contador > 0:
        pistas.append(contador)
        contador = 0

    return pistas

def generar_whitelist(solucion: list) -> list:

    '''
    Genera una whitelist 
    de los indices 'solucion' 
    de la matriz de la imagen.

    Arg: solucion -> para recorrerla.

    Return: Lista de indices en pares ordenados, cada uno en TUPLA.
    '''

    whitelist = []

    for i in range(len(solucion)):
        for j in range(len(solucion[i])):
            if solucion[i][j] == 1:
                whitelist.append((i, j))

    return whitelist

def procesar_click(coords: tuple, es_click_izq: bool, whitelist, coords_visitadas):
    '''
    La idea es procesar el click y segun el resultado accionar un acierto
    o un error. (Se puede agregar que la casilla quede en estado pendiente, si la coordenada
    no se agrega a coords_visitadas)

    Arg: coords -> viene del main y de otra funcion
         es_click_izq -> True si es
                            False si no
        whitelist -> lista de tuplas con n,m 'solucion' para recorrer
        coords_visitadas -> lista inicializada en el main para verificar
                            las coordenadas que ya han sido iteradas
    '''

    #si ya se evaluo antes no hacemos nada
    if coords in coords_visitadas:
        return None

    #ver si la celda pertenece a la solucion
    esta_en_solucion = False
    if coords in whitelist:
        esta_en_solucion = True

    #click izquierdo
    if es_click_izq:

        if esta_en_solucion:

            #agrego la coordenada porque la solucion ya es absoluta
            coords_visitadas.add(coords)
            
            return "acierto"
        
        else:
            return "error"

    #click derecho
    else:

        if not esta_en_solucion:

            #agrego la coordenada porque la solucion ya es absoluta
            coords_visitadas.add(coords)

            return "acierto"
        else:
            return "error" #es un error pendiente

def registrar_usuario(usuario: any, ruta: any):
    '''
    Registro al usuario en un archivo.

    Arg: ruta -> str: ruta del archivo de registro
         usuario -> nombre del usuario o variable
    '''

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        archivo.write(usuario + "\n")

def accionar_win_o_perdida(ventana: any, sonido: any, texto: str, color: tuple):
    '''
    Acciona configuraciones de win.

    Arg: sonido -> recibe el sonido
        ventana -> pantalla surface
        texto -> texto dependiendo si gana o pierde
        color -> para el texto en tupla RGB
    '''

    fuente = pygame.font.SysFont("Consolas", 20, bold = True, italic = False)

    sonido.set_volume(0.2)
    sonido.play()
    dibujar_texto(texto, fuente, color, 260, 500, ventana)
    pygame.display.update()
    pygame.time.delay(5000)