from nussinov import nussinov
from scoring import evaluar_algoritmo

secuencias = [
    "GGGAAAUCC",
    "GCAUCUAUGC",
    "GGGGAAAACCCC"
]

for seq in secuencias:
    resultado = evaluar_algoritmo(nussinov, seq)
    print(resultado)