from src.fasta_parser import leer_fasta
from src.nussinov import nussinov
from src.traceback_nussinov import traceback
from src.utils import ejecutar_viennarna, pares_a_dot_bracket
from src.bruteforce import max_pares_fuerza_bruta


def ejecutar_demo(secuencia):
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura = pares_a_dot_bracket(len(secuencia), pares)
    score = matriz[0][len(secuencia) - 1] if secuencia else 0

    estructura_vienna, energia = ejecutar_viennarna(secuencia)

    print("\n==============================")
    print(f"Secuencia: {secuencia}")
    print(f"Longitud: {len(secuencia)}")

    print(f"\nNussinov : {estructura}")
    print(f"Nussinov Pares : {len(pares)}")
    print(f"Nussinov Score: {score:.2f}\n")

    if len(secuencia) <= 100:
        score_bruto, pares_bruto = max_pares_fuerza_bruta(secuencia)
        print(f"Bruteforce: {pares_a_dot_bracket(len(secuencia), pares_bruto)}")
        print(f"BruteForce Pares: {len(pares_bruto)}")
        print(f"BruteForce Score: {score_bruto:.2f}\n")
        print(f"Coincide óptimo: {abs(score_bruto - score) <= 1e-9}")

    print(f"\nViennaRNA: {estructura_vienna}")
    print(f"ViennaRNA Pares: {estructura_vienna.count('(')}")
    if energia is not None:
        print(f"Energía ViennaRNA: {energia:.2f}")
    else:
        print("Energía ViennaRNA: no disponible")


if __name__ == "__main__":
    secuencias = leer_fasta("data/raw/web_inputs/examples/ejemplo.fasta")

    for nombre, secuencia in secuencias:
        ejecutar_demo(secuencia)
