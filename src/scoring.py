import time

def evaluar_algoritmo(funcion, secuencia):
    inicio = time.time()
    matriz = funcion(secuencia)
    fin = time.time()

    return {
        "longitud": len(secuencia),
        "pares": matriz[0][len(secuencia)-1],
        "tiempo": fin - inicio
    }