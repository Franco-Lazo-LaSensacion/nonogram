import pygame
from pygame import mixer
from graficos import *
from paquete import *

pygame.init()
mixer.init()

mixer.music.load("sonidos/linkinpark.mp3")
mixer.music.play()
mixer.music.set_volume(0.1)
fuente = pygame.font.SysFont("Consolas", 20, bold = True, italic = False)
sonido, sonido2, sonido3 = cargar_sonidos()
icono1, background = cargar_imagenes()
ventana = pygame.display.set_mode((ANCHO, ALTO))
rutas = ["graficos/archivos/corazon.csv", "graficos/archivos/hongo_malvado.csv",
         "graficos/archivos/triangulo.csv", "graficos/archivos/espadas.csv"]
nombres = ["corazao", "el hongoneitor", "triangulito 3000", "entre la espada y la pared"]
indice_ruta = seleccionar_indice_random(rutas)

matriz_solucion = convertir_csv_matriz(rutas[indice_ruta])

pygame.display.set_caption("Nonograma Espacial")
pygame.display.set_icon(icono1)

whitelist = generar_whitelist(matriz_solucion)
contador_aciertos = len(whitelist) #contador para caso win
counter = 0 #contador para caso win
grilla_interactiva, x_base, y_base = crear_grilla(matriz_solucion, ventana)
limite_derecho = x_base + len(grilla_interactiva[0]) * config.tam_celda #para calculo de rango
limite_inferior = y_base + len(grilla_interactiva) * config.tam_celda #para calculo de rango
coords_visitadas = set() #coordenadas visitadas ya no volves a chequear
celdas_bloqueadas = set() #celdas acertadas ya no volves a iterar
errores_pendientes = {} #error pendiente se puede borrar
matriz_pistas_filas = generar_matriz_pistas(matriz_solucion, True)
matriz_pistas_columnas = generar_matriz_pistas(matriz_solucion, False)
vidas, corazones = iniciar_vidas(3) #inicio vidas
boton_start, boton_exit, boton_ranking = crear_botones_menu(crear_boton) #creo 3 botones
nombre_usuario = "" #nombre usuario variable

banderas = {"programa_activo": True,
            "jugando": True,
            "en_menu": True,
            "en_registro": True
                }

while banderas["programa_activo"]:
        
    while banderas["en_menu"]:

        ventana.blit(background, (0, 0)) #imprimo en pantalla un fondo
        dibujar_texto("RANKING", fuente, BLANCO_CREMA, 80, 545, ventana) #dibujo texto al lado del boton ranking
        
        if actualizar_pantalla(boton_start, ventana): #los botones estan en if porque retornan una accion
            sonido.play()
            accionar_banderas(banderas, "cerrar menu")

        if actualizar_pantalla(boton_exit, ventana):
            sonido.play()
            accionar_banderas(banderas, "quit")

        if actualizar_pantalla(boton_ranking, ventana):
            sonido.play()
            ventana.blit(background, (0, 0))  #imprimo en pantalla un fondo
            mostrar_ranking(ventana, "datos/records.csv")
            dibujar_texto("Click en cualquier lado para volver atras", fuente, GRIS, 120, 545, ventana)
            pygame.display.update()
            esperando = True

            while esperando:
                for evento in pygame.event.get():

                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        sonido.play()
                        esperando = False

                    if evento.type == pygame.QUIT:
                        accionar_banderas(banderas, "quit")
                        esperando = False

        for evento in pygame.event.get():
            match evento.type: 

                case pygame.QUIT:
                    accionar_banderas(banderas, "quit")

        pygame.display.update()

    while banderas["en_registro"]:
        
        ventana.blit(background, (0, 0)) #imprimo en pantalla un fondo
        texto_ingresado_rect = pygame.Rect(360, 545, 150, 40) #inicializo rect para mostrar texto
        dibujar_texto("Ingrese su nombre de usuario: ", fuente, GRIS, 30, 545, ventana) #dibujo texto al lado del boton ranking

        for evento in pygame.event.get():
            match evento.type: 

                case pygame.QUIT:
                    accionar_banderas(banderas, "quit")

                case pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        nombre_usuario = nombre_usuario[0: -1]
                    elif evento.key == pygame.K_RETURN:   
                        registrar_usuario(nombre_usuario, "datos/registros.csv")
                        accionar_banderas(banderas, "registro")
                    else:
                        nombre_usuario += evento.unicode

        texto_sup = fuente.render(nombre_usuario, True, GRIS)
        ventana.blit(texto_sup, texto_ingresado_rect)

        pygame.display.update()

    tiempo_inicial = pygame.time.get_ticks() #creando tiempo inicio

    while banderas["jugando"]:

        ventana.blit(background, (0, 0)) #imprimo en pantalla un fondo
        
        tiempo_actual = pygame.time.get_ticks() #creando tiempo actual

        tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000 #creando tiempo transcurrido
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60

        dibujar_texto(f"Usuario: {nombre_usuario}", fuente, GRIS, 10, 10, ventana) #mostrar nombre de usuario actual
        dibujar_texto(f"Tiempo: {minutos:02d}:{segundos:02d}", fuente, GRIS, 10, 30, ventana) #mostrar clock
    
        for coord, tiempo in list(errores_pendientes.items()): # caso delay en lin.195 capturo error pendiente
            if tiempo_actual - tiempo >= config.TIEMPO_DELAY: 
                vidas -= 1
                celdas_bloqueadas.add(coords)
                del errores_pendientes[coord]

        dibujar_grilla(ventana, grilla_interactiva) #dibujo grilla
        for i in range(vidas): #dibujo vidas
            actualizar_pantalla(corazones[i], ventana)
        mostrar_todas_filas(ventana, matriz_pistas_filas, x_base, y_base) #dibujo pistas
        mostrar_todas_columnas(ventana, matriz_pistas_columnas, x_base, y_base)

        for evento in pygame.event.get():
            match evento.type: 

                case pygame.QUIT:
                    accionar_banderas(banderas, "quit")

                case pygame.MOUSEBUTTONDOWN:
                    sonido.play() #sonido click
                    funciones = pintar_celda, blanquear_celda, pintar_cruz
                    pos = pygame.mouse.get_pos()

                    x, y = pos #capturo las coordenadas mientras este en el rango de la grilla
                    if x > x_base and x < limite_derecho and y > y_base and y < limite_inferior: 
                            coords = mapear_coordenadas(grilla_interactiva, pos)
                    else:
                        coords = None

                    match evento.button:
                        case 1:

                            if coords in celdas_bloqueadas:
                                break
                            
                            verificar_estado_celda(grilla_interactiva, pos, evento.button, funciones) #aplico paradigma funcional

                            if coords is not None: #para que no rompa
                                resultado = procesar_click(coords, True, whitelist, coords_visitadas)

                                if resultado == "acierto":
                                    counter += 1
                                    celdas_bloqueadas.add(coords)

                                    if coords in errores_pendientes:
                                        del errores_pendientes[coords]

                                elif resultado == "error":
                                    errores_pendientes[coords] = pygame.time.get_ticks()

                            if counter == contador_aciertos: #caso win
                                dibujo = nombres[indice_ruta]
                                registrar_nuevo_record(nombre_usuario, tiempo_transcurrido, dibujo)
                                accionar_win_o_perdida(ventana, sonido2, "¡¡ HAS GANADO !!", VERDE)
                                accionar_banderas(banderas, "quit")

                        case 3:
                            if coords in celdas_bloqueadas:
                                break
                            
                            verificar_estado_celda(grilla_interactiva, pos, evento.button, funciones) #aplico paradigma funcional

                            if coords is not None: #hago que solo ingrese al sistema de verificaciones si las coordenadas tienen un valor
                                resultado = procesar_click(coords, False, whitelist, coords_visitadas)

                                if resultado == "error":
                                    errores_pendientes[coords] = pygame.time.get_ticks() #guardo coords y ticks

        if vidas == 0: #caso lose
            accionar_win_o_perdida(ventana, sonido3, "¡¡ GAME OVER :( !!", ROJO)
            accionar_banderas(banderas, "quit")

        pygame.display.update()

pygame.quit()
