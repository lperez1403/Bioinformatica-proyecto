from src.nussinov import nussinov


def test_matriz_dimensiones():
    secuencia = "AUGC"
    matriz = nussinov(secuencia)

    assert len(matriz) == len(secuencia)
    assert len(matriz[0]) == len(secuencia)


def test_secuencia_vacia():
    secuencia = ""
    matriz = nussinov(secuencia)

    assert matriz == []


def test_secuencia_sin_pares():
    secuencia = "AAAA"
    matriz = nussinov(secuencia)

    assert matriz[0][-1] == 0


def test_respeta_longitud_minima_de_loop():
    secuencia = "AUAU"
    matriz = nussinov(secuencia)

    assert matriz[0][-1] == 0


def test_permite_pares_si_hay_bucle_suficiente():
    secuencia = "AGGCU"
    matriz = nussinov(secuencia)

    assert matriz[0][-1] > 0
