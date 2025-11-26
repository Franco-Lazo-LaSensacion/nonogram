import pygame
from pygame import mixer
from graficos import *
from paquete import *

pygame.init()
mixer.init()

mixer.music.load("sonidos/linkinpark.mp3")
mixer.music.play()
mixer.music.set_volume(0.1)
sonido = pygame.mixer.Sound("sonidos/click1.mp3")
sonido2 = pygame.mixer.Sound("sonidos/win.mp3")
sonido3 = pygame.mixer.Sound("sonidos/lose.mp3")

ventana = pygame.display.set_mode((ANCHO, ALTO))
icono1 = pygame.image.load("graficos/imagenes/icon1.jpg")
background = pygame.image.load("graficos/imagenes/background1.png")
# background_escalado = pygame.transform.scale(background,
#                                             (1280, 900))

rutas = ["graficos/archivos/corazon.csv", "graficos/archivos/hongo_malvado.csv",
         "graficos/archivos/triangulo.csv", "graficos/archivos/espadas.csv"]
nombres = ["coração", "el hongoneitor", "triangulito 3000", "entre la espada y la pared"]
indice_ruta = seleccionar_indice_random(rutas)

matriz_solucion = convertir_csv_matriz(rutas[indice_ruta])

pygame.display.set_caption("Nonograma Espacial")
pygame.display.set_icon(icono1)

whitelist = generar_whitelist(matriz_solucion)
contador_aciertos = len(whitelist)
counter = 0
estado_error = False
grilla_interactiva, x_base, y_base = crear_grilla(matriz_solucion, ventana)
tam_celda = 27
limite_derecho = x_base + len(grilla_interactiva[0]) * tam_celda
limite_inferior = y_base + len(grilla_interactiva) * tam_celda
coords_visitadas = set()
celdas_bloqueadas = set()
errores_pendientes = {}
TIEMPO_DELAY = 3000
matriz_pistas_filas = generar_matriz_pistas(matriz_solucion, True)
matriz_pistas_columnas = generar_matriz_pistas(matriz_solucion, False)
vidas, corazones = iniciar_vidas(3)


#cargando las imagenes de los botones
boton_start = crear_boton(190, 200, 150, 100, "graficos/imagenes/start_btn.png")
boton_exit = crear_boton(360, 200, 150, 100, "graficos/imagenes/exit_btn.png")
boton_ranking = crear_boton(10, 500, 75, 75, "graficos/imagenes/ranking_btn.png")

#crear fuente para botones
fuente = pygame.font.SysFont("Consolas", 20, bold = True, italic = False)

#nombre usuario variable
nombre_usuario = ""

programa_activo = True
jugando = True
en_menu = True
en_registro = True

while programa_activo:
        
    while en_menu:

        #imprimo en pantalla un fondo
        ventana.blit(background,
                (0, 0))
        
        #dibujo texto al lado del boton ranking
        dibujar_texto("RANKING", fuente, BLANCO_CREMA, 80, 545, ventana)
        
        if actualizar_pantalla(boton_start, ventana):
            sonido.play()
            en_menu = False
        if actualizar_pantalla(boton_exit, ventana):
            sonido.play()
            en_menu = False
            jugando = False
            en_registro = False
            programa_activo = False
        if actualizar_pantalla(boton_ranking, ventana):
            sonido.play()
            ventana.blit(background,
                (0, 0))
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
                        esperando = False
                        jugando = False
                        programa_activo = False

        for evento in pygame.event.get():

            match evento.type: 

                case pygame.QUIT:

                    en_menu = False
                    jugando = False
                    programa_activo = False
                    en_registro = False

        pygame.display.update()

    
    while en_registro:
        
        #imprimo en pantalla un fondo
        ventana.blit(background,
                (0, 0))
        
        #inicializo rect para mostrar texto
        texto_ingresado_rect = pygame.Rect(360, 545, 150, 40)

        #dibujo texto al lado del boton ranking
        dibujar_texto("Ingrese su nombre de usuario: ", fuente, GRIS, 30, 545, ventana)

        for evento in pygame.event.get():

            match evento.type: 

                case pygame.QUIT:

                    en_menu = False
                    jugando = False
                    programa_activo = False
                    en_registro = False

                case pygame.KEYDOWN:
            
                    if evento.key == pygame.K_BACKSPACE:
                        nombre_usuario = nombre_usuario[0: -1]
                    elif evento.key == pygame.K_RETURN:   
                        registrar_usuario(nombre_usuario, "datos/registros.csv")
                        en_registro = False
                    else:
                        nombre_usuario += evento.unicode

        texto_sup = fuente.render(nombre_usuario, True, GRIS)
        ventana.blit(texto_sup, texto_ingresado_rect)

        pygame.display.update()

    #creando tiempo inicio
    tiempo_inicial = pygame.time.get_ticks()

    while jugando:

        #imprimo en pantalla un fondo
        ventana.blit(background,
                (0, 0))
        
        #creando tiempo actual
        tiempo_actual = pygame.time.get_ticks()

        #creando tiempo transcurrido
        tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60

        #mostrar nombre de usuario actual
        dibujar_texto(f"Usuario: {nombre_usuario}", fuente, GRIS, 10, 10, ventana)
        #mostrar clock
        dibujar_texto(f"Tiempo: {minutos:02d}:{segundos:02d}", fuente, GRIS, 10, 30, ventana)
    
        for coord, tiempo in list(errores_pendientes.items()):
            if tiempo_actual - tiempo >= TIEMPO_DELAY:

                # penalizacion por no corregir la celda
                vidas -= 1
                del errores_pendientes[coord]

        
        #Dibujo grilla, dibujo vidas, dibujo pistas
        dibujar_grilla(ventana, grilla_interactiva)
        for i in range(vidas):
            actualizar_pantalla(corazones[i], ventana)
        mostrar_todas_filas(ventana, matriz_pistas_filas, x_base, y_base)
        mostrar_todas_columnas(ventana, matriz_pistas_columnas, x_base, y_base)

        for evento in pygame.event.get():

            match evento.type: 

                case pygame.QUIT:

                    jugando = False
                    programa_activo = False

                case pygame.MOUSEBUTTONDOWN:

                    sonido.play()

                    pos = pygame.mouse.get_pos()
                    estado = verificar_estado_celda(grilla_interactiva, pos)

                    #capturo las coordenadas mientras este en el rango de la grilla
                    x, y = pos
                    if x > x_base and x < limite_derecho and y > y_base and y < limite_inferior:
                            coords = mapear_coordenadas(grilla_interactiva, pos)
                            # print("coords:", coords)
                            # print("whitelist:", whitelist)
                    else:
                        coords = None

                    match evento.button:

                        case 1:

                            if coords in celdas_bloqueadas:
                                break

                            if estado:
                                pintar_celda(grilla_interactiva, pos) #################3###############################
                            else:
                                blanquear_celda(grilla_interactiva, pos)

                            #hago que solo ingrese al sistema de verificaciones si las coordenadas tienen un valor
                            if coords is not None:
                                
                                resultado = procesar_click(coords, True, whitelist, coords_visitadas)

                                if resultado == "acierto":
                                    counter += 1
                                    celdas_bloqueadas.add(coords)

                                    if coords in errores_pendientes:
                                        del errores_pendientes[coords]

                                elif resultado == "error":
                                    errores_pendientes[coords] = pygame.time.get_ticks()

                            #si gana guardo los datos y le cierro el juego
                            if counter == contador_aciertos:
                                dibujo = nombres[indice_ruta]
                                registrar_nuevo_record(nombre_usuario, tiempo_transcurrido, dibujo)
                                sonido2.set_volume(0.2)
                                sonido2.play()
                                dibujar_texto("¡¡ HAS GANADO !!", fuente, VERDE, 260, 500, ventana)
                                pygame.display.update()
                                pygame.time.delay(5000)
                                en_menu = False
                                en_registro = False
                                jugando = False
                                programa_activo = False

                        case 3:

                            if coords in celdas_bloqueadas:
                                break

                            if estado:
                                pintar_cruz(grilla_interactiva, pos)
                            else:
                                blanquear_celda(grilla_interactiva, pos)

                            #hago que solo ingrese al sistema de verificaciones si las coordenadas tienen un valor
                            if coords is not None:

                                resultado = procesar_click(coords, False, whitelist, coords_visitadas)

                                if resultado == "error":
                                    
                                    errores_pendientes[coords] = pygame.time.get_ticks() #usar esas coordenadas para realizar el cambio y volverlo valido

                               #cancelar castigo si se corrige caso celda vacia

                            #la celda queda vacia despues de corregir?
                            celda_vacia = (verificar_estado_celda(grilla_interactiva, pos) == False)

                            #esta celda tenia que estar vacia? (no esta en whitelist)
                            celda_debe_estar_vacia = coords not in whitelist

                            #si era error pendiente y ahora quedo vacia (correcta), cancelar castigo
                            if coords in errores_pendientes and celda_debe_estar_vacia and celda_vacia:
                                del errores_pendientes[coords]
        if vidas == 0:
            sonido3.set_volume(0.2)
            sonido3.play()
            dibujar_texto("¡¡ GAME OVER :( !!", fuente, ROJO, 260, 500, ventana)
            pygame.display.update()
            pygame.time.delay(5000)
            en_menu = False
            en_registro = False
            jugando = False
            programa_activo = False

        pygame.display.update()

pygame.quit()
