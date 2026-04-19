from src.utils import (
    DEFAULT_LONG_LOOP_PENALTY,
    DEFAULT_LONG_LOOP_THRESHOLD,
    DEFAULT_MIN_LOOP_LENGTH,
    score_emparejamiento,
)


def max_pares_fuerza_bruta(
    secuencia,
    min_loop_length=DEFAULT_MIN_LOOP_LENGTH,
    long_loop_threshold=DEFAULT_LONG_LOOP_THRESHOLD,
    long_loop_penalty=DEFAULT_LONG_LOOP_PENALTY,
):
    n = len(secuencia)
    memo = {}

    def resolver(i, j):
        if i >= j:
            return 0.0, []

        if (i, j) in memo:
            return memo[(i, j)]

        mejor_valor, mejor_pares = resolver(i + 1, j)

        for k in range(i + 1, j + 1):
            score_par = score_emparejamiento(
                secuencia,
                i,
                k,
                min_loop_length=min_loop_length,
                long_loop_threshold=long_loop_threshold,
                long_loop_penalty=long_loop_penalty,
            )
            if score_par is not None:
                izquierda_valor, izquierda_pares = resolver(i + 1, k - 1)
                derecha_valor, derecha_pares = resolver(k + 1, j)

                total_valor = score_par + izquierda_valor + derecha_valor
                total_pares = [(i, k)] + izquierda_pares + derecha_pares

                if total_valor > mejor_valor:
                    mejor_valor = total_valor
                    mejor_pares = total_pares

        memo[(i, j)] = (mejor_valor, mejor_pares)
        return memo[(i, j)]

    valor, pares = resolver(0, n - 1)
    return valor, sorted(pares)
