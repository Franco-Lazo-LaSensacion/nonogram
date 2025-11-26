import pygame
from graficos import config

def registrar_record(usuario: any, tiempo: any, dibujo: str, ruta: any):
    '''
    Registro al usuario en un archivo.

    Arg: ruta -> str: ruta del archivo de registro
         usuario -> nombre del usuario o variable
    '''

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        archivo.write(f"{usuario},{tiempo},{dibujo} \n")

def cargar_records(ruta: any) -> list:
    '''
    La idea es pasar el archivo de records a una lista. 

    Arg: ruta -> ruta del archivo records

    Return: una lista para despues ordenar
    '''

    records = []

    with open(ruta, "r") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")

            if len(partes) == 2:
                
                nombre, tiempo = partes
                dibujo = ""

            elif len(partes) == 3:

                nombre, tiempo, dibujo = partes

            else:
                
                continue

            tiempo = int(tiempo)
            records.append((nombre, tiempo, dibujo))
            
    return records

def ordenar_x_burbujeo(lista: list) -> list:
    '''
    Recibe una lista y la ordena de forma ASC.

    Arg: lista -> tipo lista p/ recorrer

    Return: lista ordenada ASC.
    '''

    n = len(lista)

    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j][1] > lista[j + 1][1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    return lista

def recortar_lista(lista: list) -> list:
    '''
    Recibe una lista y la recorta.
    Solo hasta el TOP 10 esta funcion esta hecha especial para el ranking

    Arg: lista para recortar con slicing

    Return: lista recortada
    '''

    return lista[:10]

def guardar_records(records: list, ruta: any):
    '''
    Guarda los records en un archivo.

    Arg: records -> recibe la lista para recorrerla
         ruta -> ruta destino de archivo donde va ser guardado los records
    '''
    with open(ruta, "w") as archivo:
        for nombre, tiempo, dibujo in records:
            archivo.write(f"{nombre},{tiempo},{dibujo}\n")

def registrar_nuevo_record(nombre: any, tiempo: any, dibujo: any):
    '''
    Lee el archivo records, le agrega el nuevo, lo ordena,
    lo recorta y lo guarda.

    Arg: nombre -> usuario
         tiempo -> tiempo de realizacion
    '''
    records = cargar_records("datos/records.csv")
    records.append((nombre, int(tiempo), dibujo))
    ordenar_x_burbujeo(records)
    records = recortar_lista(records)
    guardar_records(records, "datos/records.csv") 

def mostrar_ranking(ventana: any, ruta: any):
    """
    Dibuja en pantalla el ranking TOP 10.
    """

    #cargar
    records = cargar_records(ruta)
    ordenar_x_burbujeo(records)
    records = recortar_lista(records)

    #fuente
    fuente_titulo = pygame.font.SysFont("Arial", 40, True)
    fuente = pygame.font.SysFont("Arial", 30)

    #texto
    texto_titulo = fuente_titulo.render("RANKING TOP 10", True, config.VERDE)
    ventana.blit(texto_titulo, (200, 80))

    #mostrar cada record
    pos_y = 150
    indice = 1

    for record in records:
        nombre = record[0]
        tiempo = record[1]
        dibujo = record[2]

        linea = f"{indice}. {nombre} - {tiempo} seg - en dibujo: {dibujo}"
        texto = fuente.render(linea, True, config.BLANCO)
        ventana.blit(texto, (100, pos_y))

        pos_y += 40
        indice += 1
