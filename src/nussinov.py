from src.utils import (
    DEFAULT_LONG_LOOP_PENALTY,
    DEFAULT_LONG_LOOP_THRESHOLD,
    DEFAULT_MIN_LOOP_LENGTH,
    score_emparejamiento,
)


def inicializar_matriz(n):
    return [[0 for _ in range(n)] for _ in range(n)]


def nussinov(
    secuencia,
    min_loop_length=DEFAULT_MIN_LOOP_LENGTH,
    long_loop_threshold=DEFAULT_LONG_LOOP_THRESHOLD,
    long_loop_penalty=DEFAULT_LONG_LOOP_PENALTY,
):
    n = len(secuencia)
    matriz = inicializar_matriz(n)

    for longitud in range(1, n):
        for i in range(n - longitud):
            j = i + longitud

            score_par = score_emparejamiento(
                secuencia,
                i,
                j,
                min_loop_length=min_loop_length,
                long_loop_threshold=long_loop_threshold,
                long_loop_penalty=long_loop_penalty,
            )

            abajo = matriz[i + 1][j]
            izquierda = matriz[i][j - 1]
            diagonal = matriz[i + 1][j - 1]
            if score_par is not None:
                diagonal += score_par

            mejor = max(abajo, izquierda, diagonal)

            # División en subproblemas
            for k in range(i + 1, j):
                mejor = max(mejor, matriz[i][k] + matriz[k + 1][j])

            matriz[i][j] = mejor

    return matriz
