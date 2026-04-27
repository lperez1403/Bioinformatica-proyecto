from src.nussinov import nussinov
from src.traceback_nussinov import traceback
from src.utils import pares_a_dot_bracket

secuencia = "AUGCGGAU"

matriz = nussinov(secuencia)
pares = traceback(matriz, secuencia, 0, len(secuencia)-1, [])

estructura = pares_a_dot_bracket(len(secuencia), pares)

print("Secuencia:", secuencia)
print("Estructura:", estructura)
print("Score:", matriz[0][len(secuencia)-1])