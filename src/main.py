from src.fasta_parser import leer_fasta
from src.nussinov import nussinov
from src.traceback_nussinov import traceback
from src.utils import pares_a_dot_bracket
from src.bruteforce import max_pares_fuerza_bruta
import RNA


def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia


def ejecutar_demo(secuencia):
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura = pares_a_dot_bracket(len(secuencia), pares)

    estructura_vienna, energia = ejecutar_viennarna(secuencia)

    print("\n==============================")
    print(f"Secuencia: {secuencia}")
    print(f"Longitud: {len(secuencia)}")

    print(f"\nNussinov : {estructura}")
    print(f"Pares Nussinov: {len(pares)}")

    if len(secuencia) <= 100:
        max_bruto, _ = max_pares_fuerza_bruta(secuencia)
        print(f"BruteForce pares: {max_bruto}")
        print(f"Coincide óptimo: {max_bruto == len(pares)}")

    print(f"\nViennaRNA: {estructura_vienna}")
    print(f"Energía ViennaRNA: {energia:.2f}")


if __name__ == "__main__":
    secuencias = leer_fasta("data/raw/ejemplo.fasta")

    for nombre, secuencia in secuencias:
        ejecutar_demo(secuencia)