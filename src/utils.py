
import RNA

# Comprueba si dos caracteres forman un par válido 
def es_par_valido(a, b):
    pairs = {
        ("A", "U"),
        ("U", "A"),
        ("G", "C"),
        ("C", "G")
        # pares wobble no se consideran en este caso
        # ("G", "U"), ("U", "G")
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

def contar_pares_dotbracket(estructura):
    return estructura.count("(")

def cargar_dbn_dataset(ruta_dbn):
    datos = {}

    with open(ruta_dbn, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    i = 0
    while i < len(lines):
        if lines[i].startswith("#Name"):
            nombre = lines[i].replace("#Name:", "").strip()
            secuencia = lines[i+1]
            estructura = lines[i+2]

            datos[nombre] = estructura

            i += 3
        else:
            i += 1

    return datos