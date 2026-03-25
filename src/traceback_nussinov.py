from utils import es_par_valido


def traceback(matriz, secuencia, i, j, pares):
    if i >= j:
        return pares

    if matriz[i][j] == matriz[i + 1][j]:
        return traceback(matriz, secuencia, i + 1, j, pares)

    if matriz[i][j] == matriz[i][j - 1]:
        return traceback(matriz, secuencia, i, j - 1, pares)

    if es_par_valido(secuencia[i], secuencia[j]) and matriz[i][j] == matriz[i + 1][j - 1] + 1:
        pares.append((i, j))
        return traceback(matriz, secuencia, i + 1, j - 1, pares)

    for k in range(i + 1, j):
        if matriz[i][j] == matriz[i][k] + matriz[k + 1][j]:
            traceback(matriz, secuencia, i, k, pares)
            traceback(matriz, secuencia, k + 1, j, pares)
            return pares

    return pares