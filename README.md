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
python src/main.py
```

### 3. Ejecutar los experimentos

```bash
python src/experiments.py
```

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

Los resultados muestran que:

	•	El algoritmo de Nussinov maximiza el número de emparejamientos posibles.

	•	ViennaRNA minimiza la energía libre de la estructura secundaria.

	•	Ambos métodos coinciden en secuencias altamente complementarias.

	•	En secuencias menos estables, Nussinov tiende a sobreestimar la estructura secundaria.

Se observa que el algoritmo de Nussinov tiende a sobreestimar el número de emparejamientos, ya que no considera restricciones termodinámicas. En contraste, ViennaRNA puede no predecir estructura secundaria en secuencias cortas o poco estables. Ambos métodos coinciden principalmente en secuencias altamente complementarias.