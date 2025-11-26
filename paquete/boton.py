import pygame

def crear_boton(x, y, ancho, alto, imagen):
    dict_boton = {}
    dict_boton["surface"] = pygame.image.load(imagen).convert_alpha()
    dict_boton["surface"] = pygame.transform.scale(dict_boton["surface"], (ancho, alto))
    dict_boton["rect_pos"] = pygame.Rect(x, y, 100, 100)
    dict_boton["rect"] = pygame.Rect((x+ancho/2) -10, y + 90, 40, 20)
    dict_boton["clickeado"] = False

    return dict_boton

def actualizar_pantalla(dict_boton, ventana):

    accion = False

    #detectando posicion del mouse
    pos = pygame.mouse.get_pos()

    #preguntar si hace click
    if dict_boton["rect_pos"].collidepoint(pos):

        #preguntar que click hace
        if pygame.mouse.get_pressed()[0] == 1 and dict_boton["clickeado"] == False:
            dict_boton["clickeado"] = True

            accion = True

        if pygame.mouse.get_pressed()[0] == 0:
            dict_boton["clickeado"] = False
            
    ventana.blit(dict_boton["surface"], dict_boton["rect_pos"])

    return accion