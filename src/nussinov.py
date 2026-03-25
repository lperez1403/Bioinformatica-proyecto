from utils import es_par_valido


def inicializar_matriz(n):
    return [[0 for _ in range(n)] for _ in range(n)]


def nussinov(secuencia):
    n = len(secuencia)
    matriz = inicializar_matriz(n)

    for longitud in range(1, n):
        for i in range(n - longitud):
            j = i + longitud

            emparejan = 1 if es_par_valido(secuencia[i], secuencia[j]) else 0

            abajo = matriz[i + 1][j]
            izquierda = matriz[i][j - 1]
            diagonal = matriz[i + 1][j - 1] + emparejan

            mejor = max(abajo, izquierda, diagonal)

            for k in range(i + 1, j):
                mejor = max(mejor, matriz[i][k] + matriz[k + 1][j])

            matriz[i][j] = mejor

    return matriz