"""Reconstrucción de la solución óptima a partir de la matriz de Nussinov."""

from src.utils import (
    DEFAULT_LONG_LOOP_PENALTY,
    DEFAULT_LONG_LOOP_THRESHOLD,
    DEFAULT_MIN_LOOP_LENGTH,
    DEFAULT_TOLERANCE,
    score_emparejamiento,
)


def _coincide(a, b, tolerance=DEFAULT_TOLERANCE):
    """Compara valores flotantes con una tolerancia pequeña."""
    return abs(a - b) <= tolerance


def traceback(
    matriz,
    secuencia,
    i,
    j,
    pares,
    min_loop_length=DEFAULT_MIN_LOOP_LENGTH,
    long_loop_threshold=DEFAULT_LONG_LOOP_THRESHOLD,
    long_loop_penalty=DEFAULT_LONG_LOOP_PENALTY,
):
    """Reconstruye recursivamente los pares que forman la solución óptima."""
    if i >= j:
        return pares

    # Si el valor óptimo se mantiene al descartar i, se continúa con el
    # subproblema inmediatamente inferior.
    if _coincide(matriz[i][j], matriz[i + 1][j]):
        return traceback(
            matriz,
            secuencia,
            i + 1,
            j,
            pares,
            min_loop_length=min_loop_length,
            long_loop_threshold=long_loop_threshold,
            long_loop_penalty=long_loop_penalty,
        )

    # Análogamente, si puede descartarse j sin pérdida de score, se reduce el
    # intervalo por la derecha.
    if _coincide(matriz[i][j], matriz[i][j - 1]):
        return traceback(
            matriz,
            secuencia,
            i,
            j - 1,
            pares,
            min_loop_length=min_loop_length,
            long_loop_threshold=long_loop_threshold,
            long_loop_penalty=long_loop_penalty,
        )

    score_par = score_emparejamiento(
        secuencia,
        i,
        j,
        min_loop_length=min_loop_length,
        long_loop_threshold=long_loop_threshold,
        long_loop_penalty=long_loop_penalty,
    )

    if (
        score_par is not None
        and _coincide(matriz[i][j], matriz[i + 1][j - 1] + score_par)
    ):
        pares.append((i, j))
        return traceback(
            matriz,
            secuencia,
            i + 1,
            j - 1,
            pares,
            min_loop_length=min_loop_length,
            long_loop_threshold=long_loop_threshold,
            long_loop_penalty=long_loop_penalty,
        )

    # Si ninguna de las opciones anteriores explica el óptimo, se busca la
    # partición interna k que descompone el intervalo en dos bloques.
    for k in range(i + 1, j):
        if _coincide(matriz[i][j], matriz[i][k] + matriz[k + 1][j]):
            traceback(
                matriz,
                secuencia,
                i,
                k,
                pares,
                min_loop_length=min_loop_length,
                long_loop_threshold=long_loop_threshold,
                long_loop_penalty=long_loop_penalty,
            )
            traceback(
                matriz,
                secuencia,
                k + 1,
                j,
                pares,
                min_loop_length=min_loop_length,
                long_loop_threshold=long_loop_threshold,
                long_loop_penalty=long_loop_penalty,
            )
            return pares

    return pares
