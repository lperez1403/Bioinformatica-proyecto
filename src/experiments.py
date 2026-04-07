#*from nussinov import nussinov
#from scoring import evaluar_algoritmo

secuencias = [
    "GGGAAAUCC",
    "GCAUCUAUGC",
    "GGGGAAAACCCC"
]

for seq in secuencias:
    resultado = evaluar_algoritmo(nussinov, seq)
    print(resultado)
    
  from fasta_parser import leer_fasta
from nussinov import nussinov
from scoring import evaluar_algoritmo

def ejecutar_experimento(ruta_fasta):
    secuencia = leer_fasta(ruta_fasta)
    resultado = evaluar_algoritmo(nussinov, secuencia)

    print("===================================")
    print(f"Archivo: {ruta_fasta}")
    print(f"Longitud: {resultado['longitud']}")
    print(f"Pares: {resultado['pares']}")
    print(f"Tiempo: {resultado['tiempo']:.5f} s")
    print("===================================\n")

if __name__ == "__main__":
    ejecutar_experimento("data/raw/ejemplo.fasta")