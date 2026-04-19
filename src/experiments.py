import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.bruteforce import max_pares_fuerza_bruta
from src.fasta_parser import leer_fasta
from src.nussinov import nussinov
from src.scoring import evaluar_algoritmo
from src.traceback_nussinov import traceback
from src.utils import cargar_dbn_dataset, contar_pares_dotbracket, ejecutar_viennarna


def guardar_resultados(resultados):
    os.makedirs("results", exist_ok=True)

    with open("results/resultados.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Nombre",
                "Secuencia",
                "Longitud",
                "Score_Nussinov",
                "Pares_Nussinov",
                "Pares_DBN",
                "Error_Pares_DBN",
                "Pares_ViennaRNA",
                "Error_Pares_ViennaRNA",
                "Energia_ViennaRNA",
                "Score_Bruteforce",
                "Pares_Bruteforce",
                "Coincide_Bruteforce",
                "Tiempo",
            ]
        )

        for fila in resultados:
            writer.writerow(fila)


def construir_resultado(nombre, secuencia, dbn_data):
    resultado = evaluar_algoritmo(nussinov, secuencia)
    matriz = nussinov(secuencia)
    pares_nussinov = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    num_pares_nussinov = len(pares_nussinov)

    estructura_vienna, energia_vienna = ejecutar_viennarna(secuencia)
    pares_vienna = contar_pares_dotbracket(estructura_vienna) if estructura_vienna else None

    estructura_real = dbn_data.get(nombre)
    pares_reales = contar_pares_dotbracket(estructura_real) if estructura_real else None

    if len(secuencia) <= 120:
        score_bruto, pares_bruto = max_pares_fuerza_bruta(secuencia)
        pares_bruteforce = len(pares_bruto)
        coincide_bruto = abs(score_bruto - resultado["score"]) <= 1e-9
    else:
        score_bruto = None
        pares_bruteforce = None
        coincide_bruto = None

    error_dbn = None if pares_reales is None else num_pares_nussinov - pares_reales
    error_vienna = None if pares_vienna is None else num_pares_nussinov - pares_vienna

    return {
        "Nombre": nombre,
        "Secuencia": secuencia,
        "Longitud": resultado["longitud"],
        "Score_Nussinov": resultado["score"],
        "Pares_Nussinov": num_pares_nussinov,
        "Pares_DBN": pares_reales,
        "Error_Pares_DBN": error_dbn,
        "Pares_ViennaRNA": pares_vienna,
        "Error_Pares_ViennaRNA": error_vienna,
        "Energia_ViennaRNA": energia_vienna,
        "Score_Bruteforce": score_bruto,
        "Pares_Bruteforce": pares_bruteforce,
        "Coincide_Bruteforce": coincide_bruto,
        "Tiempo": resultado["tiempo"],
        "Matriz": matriz,
    }


def escribir_log(resultados):
    os.makedirs("results/metrics", exist_ok=True)

    with open("results/metrics/log.txt", "w") as log_file:
        for r in resultados:
            log_text = (
                "===================================\n"
                f"Secuencia: {r['Nombre']}\n"
                f"Longitud: {r['Longitud']}\n\n"
                f"Nussinov → {r['Pares_Nussinov']} pares | score {r['Score_Nussinov']:.2f}\n"
                f"DBN → {r['Pares_DBN']} pares\n"
                f"Error DBN: {r['Error_Pares_DBN']}\n"
                f"ViennaRNA → {r['Pares_ViennaRNA']} pares | energía {r['Energia_ViennaRNA']}\n"
                f"Error ViennaRNA: {r['Error_Pares_ViennaRNA']}\n\n"
                f"BruteForce score → {r['Score_Bruteforce']}\n"
                f"BruteForce pares → {r['Pares_Bruteforce']}\n"
                f"Coincide óptimo: {r['Coincide_Bruteforce']}\n\n"
                f"Tiempo: {r['Tiempo']:.5f} s\n"
                "===================================\n\n"
            )
            log_file.write(log_text)


def guardar_matrices(resultados):
    os.makedirs("results/matrices", exist_ok=True)

    for r in resultados[:3]:
        np.savetxt(
            f"results/matrices/matriz_{r['Nombre']}.txt",
            r["Matriz"],
            fmt="%.2f",
        )


def generar_figuras(df):
    os.makedirs("results/figures", exist_ok=True)

    plt.figure()
    plt.scatter(df["Longitud"], df["Tiempo"])
    plt.xlabel("Longitud")
    plt.ylabel("Tiempo (s)")
    plt.title("Tiempo vs Longitud")
    plt.savefig("results/figures/tiempo_vs_longitud.png")
    plt.close()

    plt.figure()
    plt.scatter(df["Longitud"], df["Error_Pares_DBN"])
    plt.xlabel("Longitud")
    plt.ylabel("Error en pares respecto a DBN")
    plt.title("Error vs Longitud")
    plt.savefig("results/figures/error_vs_longitud.png")
    plt.close()

    plt.figure()
    plt.scatter(df["Pares_DBN"], df["Pares_Nussinov"])
    plt.xlabel("Pares DBN (real)")
    plt.ylabel("Pares Nussinov")
    plt.title("Comparación de emparejamientos")
    plt.savefig("results/figures/comparacion_pares.png")
    plt.close()

    if df["Pares_ViennaRNA"].notna().any():
        plt.figure()
        plt.scatter(df["Pares_ViennaRNA"], df["Pares_Nussinov"])
        plt.xlabel("Pares ViennaRNA")
        plt.ylabel("Pares Nussinov")
        plt.title("Nussinov vs ViennaRNA")
        plt.savefig("results/figures/comparacion_viennarna.png")
        plt.close()


def evaluar_fallo_estructural():
    secuencia = "GGGAAAUCC"
    matriz = nussinov(secuencia)
    pares_nussinov = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura_vienna, energia_vienna = ejecutar_viennarna(secuencia)

    os.makedirs("results/metrics", exist_ok=True)
    with open("results/metrics/fallo_estructural.txt", "w") as f:
        f.write("Secuencia de test: GGGAAAUCC\n")
        f.write(f"Pares Nussinov: {pares_nussinov}\n")
        f.write(f"Estructura ViennaRNA: {estructura_vienna}\n")
        f.write(f"Energia ViennaRNA: {energia_vienna}\n")
        f.write(
            "Interpretacion: este test ilustra que maximizar pares no garantiza "
            "capturar la estructura termodinamicamente mas plausible.\n"
        )


def ejecutar_experimento(ruta_fasta):
    dbn_data = cargar_dbn_dataset("data/processed/dbnFiles/dataset.dbn")
    secuencias = leer_fasta(ruta_fasta)[:100]

    resultados = [construir_resultado(nombre, secuencia, dbn_data) for nombre, secuencia in secuencias]

    escribir_log(resultados)
    guardar_matrices(resultados)
    evaluar_fallo_estructural()

    filas_csv = [
        [
            r["Nombre"],
            r["Secuencia"],
            r["Longitud"],
            r["Score_Nussinov"],
            r["Pares_Nussinov"],
            r["Pares_DBN"],
            r["Error_Pares_DBN"],
            r["Pares_ViennaRNA"],
            r["Error_Pares_ViennaRNA"],
            r["Energia_ViennaRNA"],
            r["Score_Bruteforce"],
            r["Pares_Bruteforce"],
            r["Coincide_Bruteforce"],
            r["Tiempo"],
        ]
        for r in resultados
    ]
    guardar_resultados(filas_csv)

    df = pd.DataFrame(
        [
            {
                k: v
                for k, v in r.items()
                if k != "Matriz"
            }
            for r in resultados
        ]
    )
    generar_figuras(df)


def ejecutar_experimentos():
    ejecutar_experimento("data/processed/dbnFiles/dataset.fasta")


if __name__ == "__main__":
    ejecutar_experimentos()
