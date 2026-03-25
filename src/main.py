from nussinov import inicializar_matriz
from nussinov import nussinov

if __name__ == "__main__":
    secuencia = "GGGAAAUCC"
    matriz = nussinov(secuencia)

    for fila in matriz:
        print(fila)