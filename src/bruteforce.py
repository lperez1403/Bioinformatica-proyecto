from src.utils import es_par_valido


def max_pares_fuerza_bruta(secuencia):
    n = len(secuencia)
    memo = {}

    def resolver(i, j):
        if i >= j:
            return 0, []

        if (i, j) in memo:
            return memo[(i, j)]

        mejor_valor, mejor_pares = resolver(i + 1, j)

        for k in range(i + 1, j + 1):
            if es_par_valido(secuencia[i], secuencia[k]):
                izquierda_valor, izquierda_pares = resolver(i + 1, k - 1)
                derecha_valor, derecha_pares = resolver(k + 1, j)

                total_valor = 1 + izquierda_valor + derecha_valor
                total_pares = [(i, k)] + izquierda_pares + derecha_pares

                if total_valor > mejor_valor:
                    mejor_valor = total_valor
                    mejor_pares = total_pares

        memo[(i, j)] = (mejor_valor, mejor_pares)
        return memo[(i, j)]

    valor, pares = resolver(0, n - 1)
    return valor, sorted(pares)