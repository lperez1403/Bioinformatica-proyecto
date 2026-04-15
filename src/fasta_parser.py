def leer_fasta(ruta):
    resultados = []

    with open(ruta) as f:
        nombre = None
        secuencia = ""

        for linea in f:
            linea = linea.strip()

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