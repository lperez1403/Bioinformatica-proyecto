from nussinov import nussinov
from traceback import traceback

if __name__ == "__main__":
    secuencia = "GGGAAAUCC"
    matriz = nussinov(secuencia)

    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])

    print("Secuencia:", secuencia)
    print("Número máximo de pares:", matriz[0][len(secuencia) - 1])
    print("Pares encontrados:", pares)
    print("\nMatriz:")

    for fila in matriz:
        print(fila)