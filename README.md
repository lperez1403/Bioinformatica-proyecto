# 🧬 Bioinformatica-proyecto  
## Predicción de estructura secundaria de RNA con el algoritmo de Nussinov

---

##  Objetivo

Desarrollar una herramienta en Python capaz de predecir la estructura secundaria de una secuencia de RNA mediante la implementación del algoritmo de Nussinov, y comparar sus resultados con modelos termodinámicos reales utilizando ViennaRNA.

---

##  Descripción del proyecto

Este proyecto implementa el algoritmo clásico de Nussinov basado en programación dinámica, cuyo objetivo es maximizar el número de emparejamientos válidos entre bases del RNA.

Además, se incorpora una comparación con ViennaRNA, una herramienta ampliamente utilizada en bioinformática que predice estructuras secundarias basadas en la minimización de la energía libre (MFE).

Esta comparación permite analizar las diferencias entre un modelo simplificado (Nussinov) y un modelo biológicamente más realista.

---

##  Funcionalidades

- ✔️ Lectura de secuencias en formato FASTA (una o múltiples)
- ✔️ Implementación del algoritmo de Nussinov
- ✔️ Reconstrucción de la estructura secundaria (traceback)
- ✔️ Representación en formato dot-bracket
- ✔️ Restricción de longitud mínima de loop (más realista)
- ✔️ Comparación con ViennaRNA (modelo energético)
- ✔️ Evaluación del rendimiento (tiempo de ejecución)
- ✔️ Ejecución de experimentos sobre múltiples secuencias

---

## Estructura del proyecto

```text
Bioinformatica-proyecto/
├── src/
│   ├── main.py
│   ├── experiments.py
│   ├── nussinov.py
│   ├── traceback_nussinov.py
│   ├── fasta_parser.py
│   ├── scoring.py
│   └── utils.py
├── data/
│   └── raw/
│       └── ejemplo.fasta
├── tests/
├── results/
├── requirements.txt
└── README.md
```

---

### Descripción de los archivos principales

- `main.py`: ejecuta el flujo principal del proyecto sobre las secuencias del archivo FASTA.
- `experiments.py`: permite lanzar experimentos y comparar resultados sobre varias secuencias.
- `nussinov.py`: contiene la implementación del algoritmo de Nussinov.
- `traceback_nussinov.py`: reconstruye los pares de bases óptimos a partir de la matriz.
- `fasta_parser.py`: lee secuencias desde archivos FASTA.
- `scoring.py`: mide el tiempo de ejecución y resume métricas básicas.
- `utils.py`: incluye funciones auxiliares, como validación de pares y conversión a dot-bracket.

---

## ▶️ Cómo ejecutar

### 1. Activar el entorno virtual

```bash
source .venv/bin/activate
```

### 2. Ejecutar el programa principal

```bash
python -m src.main
```

### 3. Ejecutar los experimentos

```bash
python -m src.experiments
```

### 4. Ejecutar los tests

```bash
pytest
```

⚠️ No se recomienda ejecutar los archivos directamente (por ejemplo python src/main.py), 
ya que esto puede provocar errores en los imports.


##  Instalación de dependencias

Instalar las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

Si fuera necesario instalar manualmente ViennaRNA:

```bash
pip install ViennaRNA
```

## Formato de entrada

Ejemplo de archivo FASTA:

```bash
>secuencia_1
GGGAAAUCC
>secuencia_2
GGGGAAAACCCC
>secuencia_3
GCAUCUAUGC
>secuencia_4
AUGCGCGCGC
```

## Ejemplo de salida

```bash
==============================
Secuencia: GGGAAAUCC
Nussinov : .((....))
ViennaRNA: .........
Energía: 0.0
Pares encontrados: [(1, 8), (2, 7)]

==============================
Secuencia: GGGGAAAACCCC
Nussinov : ((((....))))
ViennaRNA: ((((....))))
Energía: -5.4
Pares encontrados: [(0, 11), (1, 10), (2, 9), (3, 8)]
```

## Análisis

Los resultados muestran que el algoritmo de Nussinov maximiza el número de emparejamientos posibles entre bases compatibles, mientras que ViennaRNA prioriza la estabilidad termodinámica de la estructura secundaria mediante la minimización de la energía libre.

Se observa que ambos métodos pueden coincidir en secuencias altamente complementarias, donde la formación de pares es favorable tanto desde el punto de vista combinatorio como energético. Sin embargo, en secuencias menos estables o con múltiples configuraciones posibles, Nussinov tiende a sobreestimar la estructura secundaria, ya que no incorpora restricciones termodinámicas.

Además, la validación exacta alternativa basada en recursión con memoización permite comprobar que la implementación de Nussinov alcanza el número máximo de pares esperado. Esta validación confirma la corrección del algoritmo, incluso en aquellos casos en los que la estructura obtenida no coincide exactamente con otra solución óptima, ya que pueden existir múltiples configuraciones equivalentes con el mismo número de emparejamientos.

## Validación del algoritmo

Para verificar la corrección de la implementación, se ha desarrollado una validación exacta alternativa basada en recursión con memoización.

Esta validación resuelve el mismo problema de maximización de emparejamientos, pero mediante un enfoque top-down. A diferencia de una fuerza bruta pura, reutiliza subproblemas ya calculados, por lo que su comportamiento es mucho más eficiente.

Es importante destacar que el algoritmo de Nussinov puede generar múltiples estructuras óptimas con el mismo número de emparejamientos. Por ello, la validación no se basa en comparar la estructura exacta, sino en comprobar que el número máximo de pares coincide.

Criterio de validación:

- ✔️ Correcto → si el número de pares de Nussinov coincide con el óptimo
- ❌ Incorrecto → si el número de pares es inferior

Esto garantiza que la solución obtenida es óptima, aunque la estructura concreta pueda diferir.
## Interfaz web

Se ha desarrollado una interfaz web interactiva utilizando Flask que permite:

- Introducir secuencias manualmente
- Subir archivos FASTA
- Visualizar la estructura secundaria
- Comparar Nussinov con ViennaRNA
- Ver los emparejamientos mediante representación gráfica (arcos)

Ejecutar la aplicación web:

```bash
python app.py
```
Acceder en el navegador:

http://127.0.0.1:5000

##  Complejidad computacional

El algoritmo de Nussinov tiene:

- Complejidad temporal: O(n³)
- Complejidad espacial: O(n²)

Esto se debe a que para cada subproblema se evalúan todas las posibles particiones de la secuencia.

La validación exacta alternativa implementada mediante recursión con memoización reutiliza subproblemas ya resueltos, por lo que resulta mucho más eficiente que una fuerza bruta pura.


## Limitaciones

El algoritmo de Nussinov tiene complejidad O(n³), por lo que su uso práctico se limita a secuencias de tamaño moderado.

Por otro lado, la validación exacta implementada mediante recursión con memoización resulta mucho más eficiente que una fuerza bruta pura. Aun así, su coste aumenta con el tamaño de la secuencia y puede dejar de ser práctica en entradas muy grandes.

En cualquier caso, ViennaRNA sigue siendo la referencia más adecuada desde el punto de vista biológico, ya que incorpora un modelo termodinámico basado en energía libre.

## Diferencias entre Nussinov y ViennaRNA

No se espera coincidencia exacta entre ambas estructuras, ya que:

- Nussinov maximiza el número de pares
- ViennaRNA minimiza la energía libre (MFE)

Por ello, ViennaRNA puede devolver estructuras con menos emparejamientos pero más estables biológicamente.

Esta diferencia refleja la limitación del modelo de Nussinov, que no considera aspectos termodinámicos.

## Benchmark reproducible

Los experimentos pueden reproducirse ejecutando:

python -m src.experiments

Se utilizan secuencias de distinta longitud para medir el tiempo de ejecución.

## Dataset

Se ha utilizado un conjunto de secuencias de RNA de distintas longitudes
para evaluar el rendimiento del algoritmo.

El dataset se encuentra en:

data/ejemplo.fasta

Incluye secuencias de longitud variable para analizar el comportamiento
del algoritmo en distintos tamaños de entrada.

