import time


def evaluar_algoritmo(funcion, secuencia):
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
