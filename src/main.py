from fasta_parser import leer_fasta
from traceback_nussinov import traceback
from src.utils import pares_a_dot_bracket
from src.nussinov import nussinov
import RNA


def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia


if __name__ == "__main__":
    secuencias = leer_fasta("data/raw/ejemplo.fasta")

    for secuencia in secuencias:
        print("\n==============================")
        print("Secuencia:", secuencia)

        matriz = nussinov(secuencia)
        pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
        estructura = pares_a_dot_bracket(len(secuencia), pares)

        estructura_vienna, energia = ejecutar_viennarna(secuencia)

        print("Nussinov :", estructura)
        print("ViennaRNA:", estructura_vienna)
        print("Energía:", energia)

        print("Pares encontrados:", pares)
        print("Detalle de pares:")
        for i, j in pares:
            print(f"{i}-{j}: {secuencia[i]}-{secuencia[j]}")

        print("Número máximo de pares:", matriz[0][len(secuencia) - 1])