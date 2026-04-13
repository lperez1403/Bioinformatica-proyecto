
import RNA

# Comprueba si dos caracteres forman un par válido 
def es_par_valido(a, b):
    pairs = {
        ("A", "U"),
        ("U", "A"),
        ("G", "C"),
        ("C", "G")
    }
    return (a, b) in pairs

def pares_a_dot_bracket(longitud, pares):
    estructura = ["." for _ in range(longitud)]

    for i, j in pares:
        estructura[i] = "("
        estructura[j] = ")"

    return "".join(estructura)


def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia