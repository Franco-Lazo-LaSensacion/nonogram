import pygame

def crear_vida(x, y, ancho, alto):
    dict_corazon = {}
    dict_corazon["surface"] = pygame.image.load("graficos/imagenes/mYOaY.png")
    dict_corazon["surface"] = pygame.transform.scale(dict_corazon["surface"], (ancho, alto))
    dict_corazon["rect_pos"] = pygame.Rect(x, y, 200, 200)
    dict_corazon["rect"] = pygame.Rect((x+ancho/2) -10, y + 90, 40, 20)

    return dict_corazon

def actualizar_pantalla(dict_corazon, ventana):
    ventana.blit(dict_corazon["surface"], dict_corazon["rect_pos"])

def update(personaje, incremento_x):
    nueva_x = personaje["rect_pos"].x + incremento_x
    if (nueva_x > 0 and nueva_x < 700):
        personaje["rect_pos"].x = personaje["rect_pos"].x + incremento_x
        personaje["rect"].x = personaje["rect"].x + incremento_x