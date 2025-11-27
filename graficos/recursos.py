import pygame

def cargar_sonidos():
    return (
        pygame.mixer.Sound("sonidos/click1.mp3"),
        pygame.mixer.Sound("sonidos/win.mp3"),
        pygame.mixer.Sound("sonidos/lose.mp3")
    )

def cargar_imagenes():
    icono = pygame.image.load("graficos/imagenes/icon1.jpg")
    background = pygame.image.load("graficos/imagenes/background1.png")
    return icono, background