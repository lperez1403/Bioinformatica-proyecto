from src.nussinov import nussinov
from src.traceback_nussinov import traceback


def test_traceback_basico():
    secuencia = "GGGGCCCC"
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])

    assert len(pares) > 0


def test_traceback_sin_pares():
    secuencia = "AAAA"
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])

    assert pares == []