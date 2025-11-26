import random
from .logica import *

def convertir_csv_matriz(ruta: str)-> list:

    '''
    Convierte el archivo csv a una matriz.

    Retorno: La matriz con el contenido del archivo.
    '''
    with open(ruta) as archivo:
        matriz = []

        for linea in archivo:
            linea = linea.rstrip("\n")
            fila = []
            valores = linea.split(",")

            for valor in valores:
                if valor.isdigit():
                    fila.append(int(valor))
                else:
                    fila.append(valor)

            matriz.append(fila)

    return matriz

def seleccionar_indice_random(lista: list) -> int:
    '''
    Busca un indice aleatorio en una lista.

    Arg: recibe una lista.

    Return: retorna un entero (indice).
    
    '''

    for _ in range(len(lista)):
        indice = random.randint(0, len(lista) - 1)
        break

    return indice

def generar_matriz_pistas(matriz_solucion: list, bool: bool = True):

    '''
    La idea es generar una matriz pistas tanto para las filas como las columnas.

    Arg: matriz_solucion -> en base a la cual calculamos pistas.
         funcion -> funciones para calcular pistas.
         bool -> False para generar la matriz de columnas.
                Por defecto genera la matriz de filas.

    Return: matriz
    '''

    matriz_pistas = []

    if bool:
        for i in range(len(matriz_solucion)):
            pistas_por_fila = calcular_pistas(matriz_solucion[i])
            matriz_pistas.append(pistas_por_fila)
    else:
        for i in range(len(matriz_solucion)):
            pistas_por_columna = calcular_pistas_v2(matriz_solucion, i)
            matriz_pistas.append(pistas_por_columna)

    return matriz_pistas

def mapear_coordenadas(grilla: list, posicion_mouse: any) -> tuple|None:
                       
    '''
    La idea es mapear coordenadas de la grilla donde el usuario hace click
    y convertirlas a filas y columnas de la grilla_solucion.

    Arg: grilla -> por que voy a necesitar posiciones iniciales
            matriz -> por uso de medidas de pantalla
            spacing -> tamano de celda de grilla visual iterable
            posicion_mouse -> necesaria para colision

    Return: tupla -> indice fila e indice columna
            None -> si la grilla no fue colisionada
    '''

    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if grilla[i][j]["rect"].collidepoint(posicion_mouse):
                return (i, j)
            
    return None