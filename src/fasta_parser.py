def leer_fasta(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    secuencia = "".join(
        linea.strip()
        for linea in lineas
        if not linea.startswith(">")
    )

    return secuencia