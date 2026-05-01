"""Funciones auxiliares comunes para predicción, comparación y carga de datos."""

try:
    import RNA
except ImportError:  # ViennaRNA es opcional fuera de los experimentos comparativos
    RNA = None


DEFAULT_MIN_LOOP_LENGTH = 3
DEFAULT_LONG_LOOP_THRESHOLD = 30
DEFAULT_LONG_LOOP_PENALTY = 0.25
DEFAULT_TOLERANCE = 1e-9

def es_par_valido(a, b):
    """Comprueba si dos bases forman un emparejamiento permitido por el modelo."""
    pairs = {
        ("A", "U"),
        ("U", "A"),
        ("G", "C"),
        ("C", "G")
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
    """Asigna la puntuación local de un posible emparejamiento ``(i, j)``.

    El par se rechaza si no es válido o si no respeta la longitud mínima de loop.
    Si el loop supera un umbral fijado, se aplica una penalización ligera.
    """
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
    """Convierte una lista de pares ``(i, j)`` a notación dot-bracket."""
    estructura = ["." for _ in range(longitud)]

    for i, j in pares:
        estructura[i] = "("
        estructura[j] = ")"

    return "".join(estructura)


def ejecutar_viennarna(secuencia):
    """Ejecuta ViennaRNA si está disponible y devuelve estructura y energía."""
    if RNA is None:
        return None, None

    estructura, energia = RNA.fold(secuencia)
    return estructura, energia


def contar_pares_dotbracket(estructura):
    """Cuenta el número de pares en una estructura dot-bracket."""
    return estructura.count("(")


def cargar_dbn_dataset(ruta_dbn):
    """Carga un archivo DBN procesado y devuelve un diccionario nombre-estructura."""
    datos = {}

    with open(ruta_dbn, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    i = 0
    while i < len(lines):
        if lines[i].startswith("#Name"):
            nombre = lines[i].replace("#Name:", "").strip()
            estructura = lines[i + 2]

            datos[nombre] = estructura

            i += 3
        else:
            i += 1

    return datos
