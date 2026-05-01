"""Medición básica de tiempo y score para un algoritmo de predicción."""

import time


def evaluar_algoritmo(funcion, secuencia):
    """Ejecuta una función de predicción y resume longitud, score y tiempo."""
    inicio = time.time()
    matriz = funcion(secuencia)
    fin = time.time()

    if not secuencia:
        score = 0
    else:
        score = matriz[0][len(secuencia) - 1]

    return {
        "longitud": len(secuencia),
        "score": score,
        "tiempo": fin - inicio
    }
