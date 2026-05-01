"""Lectura de archivos FASTA usados en el proyecto."""


def leer_fasta(ruta):
    """Lee un archivo FASTA y devuelve una lista de tuplas ``(nombre, secuencia)``."""
    resultados = []

    with open(ruta) as f:
        nombre = None
        secuencia = ""

        for linea in f:
            linea = linea.strip()

            if not linea:
                continue

            if linea.startswith(">"):
                if nombre:
                    resultados.append((nombre, secuencia))

                nombre = linea[1:]
                secuencia = ""
            else:
                secuencia += linea

        if nombre:
            resultados.append((nombre, secuencia))

    return resultados
