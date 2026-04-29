# Función que lee un archivo FASTA y devuelve una lista de (nombre, secuencia)
def leer_fasta(ruta):
    resultados = []  # Lista donde se guardarán las secuencias

    with open(ruta) as f:
        nombre = None       # Nombre de la secuencia actual
        secuencia = ""      # Secuencia acumulada

        # Leer archivo línea por línea
        for linea in f:
            linea = linea.strip()  # Elimina espacios y saltos de línea

            if not linea:
                continue
            
            # Si la línea empieza por ">", es un encabezado
            if linea.startswith(">"):
                # Guardar la secuencia anterior si existe
                if nombre:
                    resultados.append((nombre, secuencia))

                # Actualizar nombre (quitando el ">")
                nombre = linea[1:]
                secuencia = ""  # Reiniciar secuencia

            else:
                # Concatenar líneas de secuencia
                secuencia += linea

        # Añadir la última secuencia al terminar
        if nombre:
            resultados.append((nombre, secuencia))

    return resultados