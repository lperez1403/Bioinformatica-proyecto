"""Implementación del algoritmo de Nussinov mediante programación dinámica."""

from src.utils import (
    DEFAULT_LONG_LOOP_PENALTY,
    DEFAULT_LONG_LOOP_THRESHOLD,
    DEFAULT_MIN_LOOP_LENGTH,
    score_emparejamiento,
)


def inicializar_matriz(n):
    """Crea la matriz dinámica cuadrada inicializada a cero."""
    return [[0 for _ in range(n)] for _ in range(n)]


def nussinov(
    secuencia,
    min_loop_length=DEFAULT_MIN_LOOP_LENGTH,
    long_loop_threshold=DEFAULT_LONG_LOOP_THRESHOLD,
    long_loop_penalty=DEFAULT_LONG_LOOP_PENALTY,
):
    """Calcula la matriz de programación dinámica para una secuencia de RNA.

    La matriz resultante almacena, en cada posición ``(i, j)``, la mejor
    puntuación alcanzable para la subsecuencia comprendida entre ``i`` y ``j``.
    """
    n = len(secuencia)
    matriz = inicializar_matriz(n)

    for longitud in range(1, n):
        for i in range(n - longitud):
            j = i + longitud

            # Se evalúa la posibilidad de emparejar los extremos del intervalo.
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

            # La última alternativa de la recurrencia consiste en partir el
            # intervalo en dos subproblemas independientes.
            for k in range(i + 1, j):
                mejor = max(mejor, matriz[i][k] + matriz[k + 1][j])

            matriz[i][j] = mejor

    return matriz
