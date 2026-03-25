

# Comprueba si dos caracteres forman un par válido 
def is_valid_pair(a, b):
    pairs = {
        ("A", "U"),
        ("U", "A"),
        ("G", "C"),
        ("C", "G")
    }
    return (a, b) in pairs