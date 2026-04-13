from src.utils import es_par_valido, pares_a_dot_bracket

def test_es_par_valido():
    assert es_par_valido("A", "U")
    assert es_par_valido("G", "C")
    assert not es_par_valido("A", "C")


def test_pares_a_dot_bracket():
    pares = [(0, 5), (1, 4)]
    estructura = pares_a_dot_bracket(6, pares)
    assert estructura == "((..))"

def test_dot_bracket():
    pares = [(0, 5), (1, 4)]
    estructura = pares_a_dot_bracket(6, pares)
    assert estructura == "((..))"