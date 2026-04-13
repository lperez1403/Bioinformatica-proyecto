def leer_fasta(ruta):
    with open(ruta, "r") as f:
        lineas = f.readlines()

    secuencia = "".join(
        linea.strip()
        for linea in lineas
        if not linea.startswith(">")
    )

    return secuencia