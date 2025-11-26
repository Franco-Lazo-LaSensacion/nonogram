def dibujar_texto(texto, fuente, texto_color, x, y, ventana):
    img = fuente.render(texto, True, texto_color)
    ventana.blit(img, (x, y))

    