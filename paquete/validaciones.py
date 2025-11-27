def verificar_estado_celda(grilla: list, posicion_mouse: tuple, click_mouse: any, funciones: any) -> bool:
    '''
    Trabaja independientemente las coordenadas, verifica si esta pintada o no.

    Arg: grilla -> principal, la interactiva
            posicion_mouse -> si hay colision guardo el estado actual de la casilla
            click_mouse -> para que segun el click haga algo
            funcion -> usar la que fuese dentro segun el estado

    Return: True -> si se puede pintar
            False -> si ya estaba pintada, para despintar
            (misma logica aplica para cruces)
    '''
    estado_actual = 0
    se_pinta = True

    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if grilla[i][j]["rect"].collidepoint(posicion_mouse):
                estado_actual = grilla[i][j]["valor"]
                

    if estado_actual == 1 or estado_actual == 3:
        funciones[1](grilla, posicion_mouse)
    else:
        if click_mouse == 1:
            funciones[0](grilla, posicion_mouse)
        else:
            funciones[2](grilla, posicion_mouse)
            
    return se_pinta

def verificar_acierto(whitelist: list, coordenadas: tuple) -> bool:
    '''
    Verifica si una coordenada obtenida del click esta en la solucion.

    Arg: whitelist -> para ver que valores estan ahi dentro
            coordenadas -> para a partir de esa tupla obtenida buscarla en la whitelist

    Return: True si la coordenada es de solucion
            False si no
    ''' 

    for tupla in whitelist:

        if coordenadas == tupla:
            return True
    return False