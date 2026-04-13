from fasta_parser import leer_fasta
from nussinov import nussinov
from scoring import evaluar_algoritmo
import RNA


def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia


def ejecutar_experimento(ruta_fasta):
    secuencia = leer_fasta(ruta_fasta)

    resultado = evaluar_algoritmo(nussinov, secuencia)
    estructura_v, energia = ejecutar_viennarna(secuencia)

    print("===================================")
    print(f"Archivo: {ruta_fasta}")
    print(f"Longitud: {resultado['longitud']}")
    print(f"Pares (Nussinov): {resultado['pares']}")
    print(f"Tiempo: {resultado['tiempo']:.5f} s")
    print(f"ViennaRNA: {estructura_v}")
    print(f"Energía: {energia}")
    print("===================================\n")


def ejecutar_experimentos():
    archivos = [
        "data/raw/ejemplo.fasta",
    ]

    for ruta in archivos:
        ejecutar_experimento(ruta)


if __name__ == "__main__":
    ejecutar_experimentos()