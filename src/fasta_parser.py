def leer_fasta(ruta):
    secuencias = []
    secuencia_actual = ""

    with open(ruta, "r") as f:
        for linea in f:
            linea = linea.strip()

            if linea.startswith(">"):
                if secuencia_actual:
                    secuencias.append(secuencia_actual)
                    secuencia_actual = ""
            else:
                secuencia_actual += linea

        if secuencia_actual:
            secuencias.append(secuencia_actual)

    return secuencias