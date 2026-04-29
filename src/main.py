from src.fasta_parser import leer_fasta
from src.nussinov import nussinov
from src.traceback_nussinov import traceback
from src.utils import ejecutar_viennarna, pares_a_dot_bracket
from src.bruteforce import max_pares_fuerza_bruta


def ejecutar_demo(secuencia):
    matriz = nussinov(secuencia)  # Calcula la matriz de programación dinámica
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])  # Obtiene los pares óptimos
    estructura = pares_a_dot_bracket(len(secuencia), pares)  # Convierte los pares a formato dot-bracket
    score = matriz[0][len(secuencia) - 1] if secuencia else 0  # Score final (valor óptimo)

    estructura_vienna, energia = ejecutar_viennarna(secuencia)  # Ejecuta ViennaRNA como referencia

    print("\n==============================")  
    print(f"Secuencia: {secuencia}")  
    print(f"Longitud: {len(secuencia)}")  

    print(f"\nNussinov : {estructura}")  
    print(f"Nussinov Pares : {len(pares)}") 
    print(f"Nussinov Score: {score:.2f}\n")  

    # Ejecutar fuerza bruta solo para secuencias pequeñas
    if len(secuencia) <= 100:
        score_bruto, pares_bruto = max_pares_fuerza_bruta(secuencia)  # Calcula solución exacta
        print(f"Bruteforce: {pares_a_dot_bracket(len(secuencia), pares_bruto)}")  
        print(f"BruteForce Pares: {len(pares_bruto)}")  
        print(f"BruteForce Score: {score_bruto:.2f}\n")  # Score brute force
        print(f"Coincide óptimo: {abs(score_bruto - score) <= 1e-9}")  # Comprueba si coincide con Nussinov

    print(f"\nViennaRNA: {estructura_vienna}")  # Estructura predicha por ViennaRNA
    print(f"ViennaRNA Pares: {estructura_vienna.count('(')}")  # Número de pares ViennaRNA

    # Mostrar energía si está disponible
    if energia is not None:
        print(f"Energía ViennaRNA: {energia:.2f}")
    else:
        print("Energía ViennaRNA: no disponible")


if __name__ == "__main__":
    secuencias = leer_fasta("data/raw/web_inputs/examples/ejemplo.fasta")  # Leer secuencias del archivo

    # Ejecutar demo para cada secuencia
    for nombre, secuencia in secuencias:
        ejecutar_demo(secuencia)
