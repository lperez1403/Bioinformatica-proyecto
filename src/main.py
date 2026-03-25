from fasta_parser import leer_fasta
from nussinov import nussinov
from traceback_nussinov import traceback
from utils import pares_a_dot_bracket

if __name__ == "__main__":
    secuencia = leer_fasta("data/raw/ejemplo.fasta")
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura = pares_a_dot_bracket(len(secuencia), pares)

    print("Secuencia: ", secuencia)
    print("Estructura:", estructura)
    print("Pares encontrados:", pares)
    print("\nDetalle de pares:")
    for i, j in pares:
        print(f"{i}-{j}: {secuencia[i]}-{secuencia[j]}")
    print("Número máximo de pares:", matriz[0][len(secuencia) - 1])