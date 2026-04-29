from src.utils import (
    DEFAULT_LONG_LOOP_PENALTY,
    DEFAULT_LONG_LOOP_THRESHOLD,
    DEFAULT_MIN_LOOP_LENGTH,
    score_emparejamiento,
)

# Función que calcula el máximo valor de emparejamientos en una secuencia
def max_pares_fuerza_bruta(
    secuencia,
    min_loop_length=DEFAULT_MIN_LOOP_LENGTH,
    long_loop_threshold=DEFAULT_LONG_LOOP_THRESHOLD,
    long_loop_penalty=DEFAULT_LONG_LOOP_PENALTY,
):
    n = len(secuencia)
    memo = {}  # Diccionario para guardar resultados ya calculados

    # Función recursiva que resuelve el problema en el intervalo [i, j]
    def resolver(i, j):
        # Caso base: si no hay intervalo válido, no hay pares
        if i >= j:
            return 0.0, []

        # Si ya se ha resuelto este subproblema, se devuelve directamente
        if (i, j) in memo:
            return memo[(i, j)]

        # Opción 1: no emparejar la posición i
        mejor_valor, mejor_pares = resolver(i + 1, j)

        # Opción 2: intentar emparejar i con cada k posible
        for k in range(i + 1, j + 1):
            # Calcula la puntuación del posible par (i, k)
            score_par = score_emparejamiento(
                secuencia,
                i,
                k,
                min_loop_length=min_loop_length,
                long_loop_threshold=long_loop_threshold,
                long_loop_penalty=long_loop_penalty,
            )

            # Si el emparejamiento no es válido, se pasa al siguiente k
            if score_par is None:
                continue  

            # Resolver recursivamente las dos subpartes:
            # izquierda: entre i+1 y k-1
            # derecha: entre k+1 y j
            izquierda_valor, izquierda_pares = resolver(i + 1, k - 1)
            derecha_valor, derecha_pares = resolver(k + 1, j)

            # Suma total de este emparejamiento
            total_valor = score_par + izquierda_valor + derecha_valor

            # Si mejora el resultado, se actualiza la mejor solución
            if total_valor > mejor_valor:
                mejor_valor = total_valor
                mejor_pares = [(i, k)] + izquierda_pares + derecha_pares

        # Guardar el resultado en memoización
        memo[(i, j)] = (mejor_valor, mejor_pares)
        return memo[(i, j)]

    # Llamada inicial sobre toda la secuencia
    valor, pares = resolver(0, n - 1)

    # Devolver valor máximo y lista de pares ordenada
    return valor, sorted(pares)