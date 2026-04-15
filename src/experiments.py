from src.fasta_parser import leer_fasta
from src.nussinov import nussinov
from src.scoring import evaluar_algoritmo
import RNA
import csv
import os
from src.utils import cargar_dbn_dataset, contar_pares_dotbracket
from src.bruteforce import max_pares_fuerza_bruta
from src.utils import pares_a_dot_bracket
import matplotlib.pyplot as plt
import pandas as pd

def guardar_resultados(resultados):
    os.makedirs("results", exist_ok=True)

    with open("results/resultados.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Nombre",
            "Secuencia",
            "Longitud",
            "Pares_Nussinov",
            "Pares_DBN",
            "Error_Pares",
            "Pares_Bruteforce",
            "Coincide_Bruteforce",
            "Tiempo"
        ])

        for r in resultados:
            writer.writerow(r)


def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia


def ejecutar_experimento(ruta_fasta):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    dbn_data = cargar_dbn_dataset("data/processed/dbnFiles/dataset.dbn")
    secuencias = leer_fasta(ruta_fasta)

    resultados_totales = []

    os.makedirs("results/metrics", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)
    os.makedirs("results/matrices", exist_ok=True)

    log_file = open("results/metrics/log.txt", "w")

    # ⚠️ limitar si quieres (para pruebas)
    secuencias = secuencias[:100]

    for idx, (nombre, secuencia) in enumerate(secuencias):

        resultado = evaluar_algoritmo(nussinov, secuencia)

        # ViennaRNA (opcional, no crítico)
        try:
            estructura_v, energia = ejecutar_viennarna(secuencia)
        except:
            estructura_v, energia = None, None

        #  BRUTE FORCE 
        if resultado['longitud'] <= 120:
            max_bruto, _ = max_pares_fuerza_bruta(secuencia)
            coincide_bruto = (max_bruto == resultado['pares'])
        else:
            max_bruto = None
            coincide_bruto = None

        #  DBN real
        estructura_real = dbn_data.get(nombre, None)

        if estructura_real:
            pares_real = contar_pares_dotbracket(estructura_real)
        else:
            pares_real = None

        #  error
        if pares_real is not None:
            error_pares = resultado['pares'] - pares_real
        else:
            error_pares = None

        #  LOG
        log_text = (
            "===================================\n"
            f"Secuencia: {nombre}\n"
            f"Longitud: {resultado['longitud']}\n\n"

            f"Nussinov → {resultado['pares']} pares\n"
            f"DBN → {pares_real} pares\n"
            f"Error DBN: {error_pares}\n\n"

            f"BruteForce → {max_bruto}\n"
            f"Coincide óptimo: {coincide_bruto}\n\n"

            f"Tiempo: {resultado['tiempo']:.5f} s\n"
            "===================================\n\n"
        )
        log_file.write(log_text)

        #  Guardar algunas matrices (solo 3 primeras)
        if idx < 3:
            matriz = nussinov(secuencia)
            np.savetxt(
                f"results/matrices/matriz_{nombre}.txt",
                matriz,
                fmt="%d"
            )

        resultados_totales.append([
            nombre,
            secuencia,
            resultado['longitud'],
            resultado['pares'],
            pares_real,
            error_pares,
            max_bruto,
            coincide_bruto,
            resultado['tiempo']
        ])

    log_file.close()

    # CSV
    guardar_resultados(resultados_totales)

    #  FIGURAS AUTOMÁTICAS
    df = pd.DataFrame(resultados_totales, columns=[
        "Nombre", "Secuencia", "Longitud", "Pares_Nussinov",
        "Pares_DBN", "Error_Pares", "Pares_Bruteforce",
        "Coincide_Bruteforce", "Tiempo"
    ])

    # Tiempo vs longitud
    plt.figure()
    plt.scatter(df["Longitud"], df["Tiempo"])
    plt.xlabel("Longitud")
    plt.ylabel("Tiempo (s)")
    plt.title("Tiempo vs Longitud")
    plt.savefig("results/figures/tiempo_vs_longitud.png")
    plt.close()

    # Error vs longitud
    plt.figure()
    plt.scatter(df["Longitud"], df["Error_Pares"])
    plt.xlabel("Longitud")
    plt.ylabel("Error en pares")
    plt.title("Error vs Longitud")
    plt.savefig("results/figures/error_vs_longitud.png")
    plt.close()

    # Comparación pares
    plt.figure()
    plt.scatter(df["Pares_DBN"], df["Pares_Nussinov"])
    plt.xlabel("Pares DBN (real)")
    plt.ylabel("Pares Nussinov")
    plt.title("Comparación de emparejamientos")
    plt.savefig("results/figures/comparacion_pares.png")
    plt.close()


def ejecutar_experimentos():
    archivos = [
        "data/processed/dbnFiles/dataset.fasta",
    ]

    for ruta in archivos:
        ejecutar_experimento(ruta)


if __name__ == "__main__":
    ejecutar_experimentos()