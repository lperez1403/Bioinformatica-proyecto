from fasta_parser import leer_fasta
from nussinov import nussinov
from traceback_nussinov import traceback
from utils import pares_a_dot_bracket
import RNA

def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia

if __name__ == "__main__":
    secuencia = leer_fasta("data/raw/ejemplo.fasta")
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura = pares_a_dot_bracket(len(secuencia), pares)
    estructura_vienna, energia = ejecutar_viennarna(secuencia)

    print("Secuencia: ", secuencia)
    print("Estructura:", estructura)
    print("Pares encontrados:", pares)
    print("\nDetalle de pares:")
    for i, j in pares:
        print(f"{i}-{j}: {secuencia[i]}-{secuencia[j]}")

    print("\nViennaRNA:")
    print("Estructura:", estructura_vienna)
    print("Energía:", energia)

    print("\nComparación:")
    print("Nussinov :", estructura)
    print("ViennaRNA:", estructura_vienna)

    print("Número máximo de pares:", matriz[0][len(secuencia) - 1])