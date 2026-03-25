def inicializar_matriz(n):
    return [[0 for _ in range(n)] for _ in range(n)]


def nussinov(secuencia):
    n = len(secuencia)
    matriz = inicializar_matriz(n)

    for longitud in range(1, n):
        for i in range(n - longitud):
            j = i + longitud

            # de momento no calculamos nada todavía
            matriz[i][j] = 0

    return matriz