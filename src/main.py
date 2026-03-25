from nussinov import nussinov

if __name__ == "__main__":
    secuencia = "GGGAAAUCC"
    matriz = nussinov(secuencia)

    print("Secuencia:", secuencia)
    print("Número máximo de pares:", matriz[0][len(secuencia) - 1])
    print("\nMatriz:")

    for fila in matriz:
        print(fila)