from src.fasta_parser import leer_fasta
from src.nussinov import nussinov
from src.scoring import evaluar_algoritmo
import RNA
import csv
import os
from src.utils import cargar_dbn_dataset, contar_pares_dotbracket
from src.bruteforce import max_pares_fuerza_bruta
from src.utils import pares_a_dot_bracket

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
    dbn_data = cargar_dbn_dataset("data/processed/dbnFiles/dataset.dbn")
    secuencias = leer_fasta(ruta_fasta)

    resultados_totales = []

    os.makedirs("results/metrics", exist_ok=True)
    log_file = open("results/metrics/log.txt", "w")

    # limitar para no procesar 70k si queremos
    secuencias = secuencias[:100]

    for idx, (nombre, secuencia) in enumerate(secuencias):
        resultado = evaluar_algoritmo(nussinov, secuencia)
        # ViennaRNA opcional (no se usa para validación)
        estructura_v, energia = ejecutar_viennarna(secuencia)

        # VALIDACIÓN BRUTE FORCE SOLO PARA SECUENCIAS "CORTAS"
        if resultado['longitud'] <= 200:
            max_bruto, pares_bruto = max_pares_fuerza_bruta(secuencia)
            coincide_bruto = (max_bruto == resultado['pares'])
        else:
            max_bruto = None
            coincide_bruto = None
        
        estructura_real = dbn_data.get(nombre, None)

        if estructura_real:
            pares_real = contar_pares_dotbracket(estructura_real)
        else:
            pares_real = None

        if pares_real is not None:
            error_pares = resultado['pares'] - pares_real
        else:
            error_pares = None

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
    guardar_resultados(resultados_totales)


def ejecutar_experimentos():
    archivos = [
        "data/processed/dbnFiles/dataset.fasta",
    ]

    for ruta in archivos:
        ejecutar_experimento(ruta)


if __name__ == "__main__":
    ejecutar_experimentos()