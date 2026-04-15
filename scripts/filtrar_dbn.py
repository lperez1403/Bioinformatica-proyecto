import os


def procesar_dbn_file(path, max_len):
    resultados = []

    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    i = 0
    while i < len(lines):
        if lines[i].startswith("#Name"):
            nombre = lines[i]

            length_line = lines[i+1]
            import re

            length_text = length_line.split(":")[1]

            # Extraer solo números
            match = re.search(r"\d+", length_text)

            if match:
                length = int(match.group())
            else:
                return []  # saltar si no hay número válido

            secuencia = lines[i+3]
            estructura = lines[i+4]

            if (
                length <= max_len
                and "[" not in estructura
                and "]" not in estructura
            ):
                resultados.append((nombre, secuencia, estructura))

            i += 5
        else:
            i += 1

    return resultados


def filtrar_todos_dbn(input_folder, output_path, max_len=120):
    todos = []

    for file in os.listdir(input_folder):
        if file.endswith(".dbn"):
            full_path = os.path.join(input_folder, file)
            #print(f"Procesando {file}...")

            resultados = procesar_dbn_file(full_path, max_len)
            todos.extend(resultados)

    # guardar resultado
    with open(output_path, "w") as f, open("data/processed/dbnFiles/dataset.fasta", "w") as f_fasta:
        for nombre, seq, struct in todos:
            # Guardar DBN
            f.write(f"{nombre}\n")
            f.write(f"{seq}\n")
            f.write(f"{struct}\n\n")

            # Guardar FASTA
            nombre_limpio = nombre.replace("#Name:", "").strip()
            f_fasta.write(f">{nombre_limpio}\n{seq}\n")

    print(f"\n✅ Total secuencias guardadas: {len(todos)}")


if __name__ == "__main__":
    filtrar_todos_dbn(
        input_folder="data/raw/dbnFiles",
        output_path="data/processed/dbnFiles/dataset.dbn",
        max_len=150
    )