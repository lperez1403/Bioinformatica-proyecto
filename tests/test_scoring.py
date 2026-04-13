from src.scoring import evaluar_algoritmo
from src.nussinov import nussinov


def test_evaluacion_basica():
    secuencia = "AUGC"
    resultado = evaluar_algoritmo(nussinov, secuencia)

    assert "longitud" in resultado
    assert "pares" in resultado
    assert "tiempo" in resultado


def test_longitud_correcta():
    secuencia = "AUGC"
    resultado = evaluar_algoritmo(nussinov, secuencia)

    assert resultado["longitud"] == 4