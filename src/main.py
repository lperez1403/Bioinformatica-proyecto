from utils import is_valid_pair
from nussinov import inicializar_matriz


if __name__ == "__main__":
    matriz = inicializar_matriz(5)
    for fila in matriz:
        print(fila)