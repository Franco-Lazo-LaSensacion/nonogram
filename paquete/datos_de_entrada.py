def obtener_digito(mensaje: str) -> int:
    '''
    Obtiene un digito

    Args: recibe mensaje (str)

    Returns: returna el entero validado        
    '''

    numero = input(mensaje)

    if len(numero) > 1:
        print("se aceptan solo numeros de 1 digito para el menu.")
        return

    for i in range(len(numero)):

        if ord(numero[i]) > 47 or ord(numero[i]) < 58:
            numero = int(numero)
            return numero