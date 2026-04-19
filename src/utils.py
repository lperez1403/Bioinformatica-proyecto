try:
    import RNA
except ImportError:  # ViennaRNA es opcional fuera de los experimentos comparativos
    RNA = None


DEFAULT_MIN_LOOP_LENGTH = 3
DEFAULT_LONG_LOOP_THRESHOLD = 30
DEFAULT_LONG_LOOP_PENALTY = 0.25
DEFAULT_TOLERANCE = 1e-9

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


def score_emparejamiento(
    secuencia,
    i,
    j,
    min_loop_length=DEFAULT_MIN_LOOP_LENGTH,
    long_loop_threshold=DEFAULT_LONG_LOOP_THRESHOLD,
    long_loop_penalty=DEFAULT_LONG_LOOP_PENALTY,
):
    if not es_par_valido(secuencia[i], secuencia[j]):
        return None

    loop_length = j - i - 1
    if loop_length < min_loop_length:
        return None

    score = 1.0
    if loop_length > long_loop_threshold:
        score -= long_loop_penalty

    return score

def pares_a_dot_bracket(longitud, pares):
    estructura = ["." for _ in range(longitud)]

    for i, j in pares:
        estructura[i] = "("
        estructura[j] = ")"

    return "".join(estructura)


def ejecutar_viennarna(secuencia):
    if RNA is None:
        return None, None

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
