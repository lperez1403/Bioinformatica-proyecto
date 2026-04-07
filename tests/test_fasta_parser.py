import os
from src.fasta_parser import leer_fasta

# Comprueba que se extrae la secuencia sin las cabeceras >
def test_leer_fasta_contenido():
    # Creamos un archivo FASTA de prueba temporal
    ruta_test = "test_temporal.fasta"
    with open(ruta_test, "w") as f:
        f.write(">Secuencia_Prueba\n")
        f.write("GCUACG\n")
    
    # Lo ejecutamos
    resultado = leer_fasta(ruta_test)
    
    # Verificamos que solo lea las letras de la secuencia 
    assert resultado == "GCUACG"
    
    # Limpiamos el archivo temporal
    os.remove(ruta_test)

# Comprueban que las secuencias se unen correctamente en lineas
def test_leer_fasta_multilinea():
    ruta_test = "test_multi.fasta"
    with os.fdopen(os.open(ruta_test, os.O_WRONLY | os.O_CREAT), 'w') as f:
        f.write(">Cabecera\n")
        f.write("GGGG\n")
        f.write("AAAA\n")
    
    resultado = leer_fasta(ruta_test)
    assert resultado == "GGGGAAAA"
    os.remove(ruta_test)