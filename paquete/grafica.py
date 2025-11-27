import pygame
from .logica import *
from .vida_llena import *
from graficos import config

def dibujar_grilla(surface: any, grilla: list)-> None:
    '''
    Muestra una grilla en pantalla.

    Arg: surface -> para tener donde imprimirla.
        grilla -> para acceder a cada elemento (en este caso diccionarios)
    
    Return: Muestra la grilla en ventana directo.
    '''
    for fila in grilla:
        for celda in fila:
            surface.blit(celda["surface"], celda["rect"])

def dibujar_cruz(celda_surface: any, color: tuple = config.ROJO, grosor: any = 2):
    '''
    Dibuja una cruz dentro de una celda.

    Arg: celda_surface -> que va a ser obtenida del diccionario

    Return: No tiene. Dibuja directo.
    '''

    an, a = celda_surface.get_size()
    pygame.draw.line(celda_surface, color, (0, 0), (an, a), grosor)
    pygame.draw.line(celda_surface, color, (an, 0), (0, a), grosor)

def pintar_cruz(grilla: list, posicion_mouse: any, funcion = dibujar_cruz):
    '''
    Realiza una cruz en la casilla colisionada.

    Arg: grilla -> para recorrerla e iterar sus elementos que vienen
                    a ser diccionarios. Los cuales cambiando una de sus
                    keys puedo marcar una cruz en la celda.
        posicion_mouse -> evento.pos, para saber donde colisionar por ende marcar cruz.

    Return: No tiene. Realiza la cruz directo.
    '''

    for fila in grilla:
        for celda in fila: 
            if celda["rect"].collidepoint(posicion_mouse):
                funcion(celda["surface"])
                celda["valor"] = 3

def pintar_celda(grilla: list, posicion_mouse: any): 
    '''
    Pinta la celda seleccionada si y solo si, existe una colision.

    Arg: grilla -> para recorrerla e iterar sus elementos que vienen
                    a ser diccionarios. Los cuales cambiando una de sus
                    keys puedo pintar la celda.
        posicion_mouse -> evento.pos, para saber donde colisionar por ende pintar.

    Return: No tiene. Pinta directo.
    '''
    for fila in grilla:
        for celda in fila: 
            if celda["rect"].collidepoint(posicion_mouse):
                celda["surface"].fill(config.NEGRO)
                celda["valor"] = 1

def blanquear_celda(grilla: list, posicion_mouse: any):
    '''
    Vacia la celda si y solo si, existe una colision.

    Arg: grilla -> para recorrerla e iterar sus elementos que vienen
                    a ser diccionarios. Los cuales cambiando una de sus
                    keys puedo blanquear la celda.
        posicion_mouse -> evento.pos, para saber donde colisionar por ende blanquear.

    Return: No tiene. Pinta directo.
    '''
    for fila in grilla:
        for celda in fila:
            if celda["rect"].collidepoint(posicion_mouse): #controlo la colision
                celda["surface"].fill(config.BLANCO)
                celda["valor"] = 0
                
def mostrar_pistas_fila(ventana: any,
                        pistas_filas: list,
                        x_base: int,
                        y_base: int,
                        tam_celda: int = 27):
    '''
    La idea es mostrar las pistas 
    (ya generadas) por cada fila de la grilla.

    Arg: ventana -> para blit de texto.
        pistas_fila -> para mostrar cada sublista 
        que vienen a ser las pistas de cada fila.

    '''
    fuente = pygame.font.SysFont("Consolas", 20, bold = True, italic = True)

    n = len(pistas_filas)
    margen = 30
    for i in range(n):
            indice = n - 1 - i # n = largo de lista, -1 para restar y convertir en ultimo elemento.
                               # -i para que vaya iterando en reversa
            numero = pistas_filas[indice]
            sup = fuente.render(str(numero), True, config.COLOR_PISTAS)
            ventana.blit(sup, (x_base-i*tam_celda-margen, y_base+3))

def mostrar_pistas_columnas(ventana: any,
                            pistas_columnas: list,
                            x_base: int,
                            y_base: int,
                            tam_celda: int = 27):
    '''
    La idea es mostrar las pistas (ya generadas) por cada columna de la grilla.

    Arg: ventana -> para blit de texto.

        pistas_columnas -> para mostrar
        cada sublista que vienen a ser las pistas de cada columna.

    '''
    fuente = pygame.font.SysFont("Consolas", 20, bold = True, italic = True)
    margen = 30  
    n = len(pistas_columnas)

    for i in range(n):
        indice = n - 1 - i # n = largo de lista, -1 para restar y convertir en ultimo elemento.
                           # -i para que vaya iterando en reversa
        numero = pistas_columnas[indice]
        sup = fuente.render(str(numero), True, (255, 165, 0))
        ventana.blit(sup, (x_base+5, y_base-i*tam_celda-margen))

def mostrar_todas_filas(ventana: any,
                        pistas_filas: list,
                        x_base: int,
                        y_base: int,
                        tam_celda = 27):
    '''
    Itera la funcion para mostrar pistas por fila con un for. 
    Debido a que las pistas vienen en matriz. Utiliza una funcion interna
    para dividir resposabilidades.


    Arg: ventana > para utilizar en funcion interna.
         pistas_filas > matriz pistas fila para recorrer.
         x_base > punto inicial en X de la grilla.
         y_base > punto inicial en Y de la grilla.
         tam_celda > tamano de celda, por defecto 27.
    '''
    for fila_pistas in pistas_filas:
        mostrar_pistas_fila(ventana, fila_pistas, x_base, y_base, tam_celda)
        y_base += tam_celda #salto de fila simetrico por tam_celda.

def mostrar_todas_columnas(ventana: any,
                           pistas_columnas: list,
                           x_base: int,
                           y_base: int,
                           tam_celda = 27):
    '''
    Itera la funcion para mostrar pistas por columna con un for. 
    Debido a que las pistas vienen en matriz. Utiliza una funcion interna
    para dividir resposabilidades.

    Arg: ventana > para utilizar en funcion interna.
         pistas_columnas > matriz pistas columnas para recorrer.
         x_base > punto inicial en X de la grilla.
         y_base > punto inicial en Y de la grilla.
         tam_celda > tamano de celda, por defecto 27.
    '''
    for columna_pistas in pistas_columnas:
        mostrar_pistas_columnas(ventana, columna_pistas, x_base, y_base, tam_celda)
        x_base += tam_celda #salto de fila simetrico por tam_celda.

def crear_botones_menu(funcion: any):
    '''
    Creo los botones del menu al mismo tiempo.

    Arg: funcion -> crear boton
    '''
    return [
        funcion(190, 200, 150, 100, "graficos/imagenes/start_btn.png"),
        funcion(360, 200, 150, 100, "graficos/imagenes/exit_btn.png"),
        funcion(10, 500, 75, 75, "graficos/imagenes/ranking_btn.png")
    ]

def iniciar_vidas(cantidad: int):
    '''
    Inicializa el sistema vidas (variable).
    Inicializa los corazones visuales.

    Arg: cantidad de vidas

    '''

    corazones = []
    vidas = cantidad
    x = 630

    for _ in range(vidas):
        corazon = crear_vida(x, 15, 30, 30)
        x -= 40
        corazones.append(corazon)
    
    return vidas, corazones