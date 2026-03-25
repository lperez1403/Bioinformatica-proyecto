

# Comprueba si dos caracteres forman un par válido 
def es_par_valido(a, b):
    pairs = {
        ("A", "U"),
        ("U", "A"),
        ("G", "C"),
        ("C", "G")
    }
    return (a, b) in pairs