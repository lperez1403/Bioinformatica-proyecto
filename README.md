# 🧬 Bioinformatica-proyecto

## Predicción de estructura secundaria de RNA con el algoritmo de Nussinov

------------------------------------------------------------------------

## Objetivo

Implementar el algoritmo de Nussinov para la predicción de estructura
secundaria de RNA y evaluarlo mediante:

-   Validación exacta en secuencias cortas
-   Comparación con estructuras reales (dataset bpRNA)
-   Análisis de rendimiento y complejidad

------------------------------------------------------------------------

## Descripción del proyecto

Este proyecto implementa el algoritmo clásico de **Nussinov**, basado en programación dinámica, cuyo objetivo es predecir la estructura secundaria de una secuencia de RNA maximizando el número de emparejamientos válidos entre bases (A-U, G-C y G-U).

El algoritmo construye una matriz de subproblemas en la que cada celda representa el número máximo de pares posibles en un subsecuencia, resolviendo el problema de forma eficiente mediante un enfoque **bottom-up**. Posteriormente, se aplica un proceso de **traceback** para reconstruir la estructura óptima en formato dot-bracket.

---

## Metodología de evaluación

El algoritmo se evalúa en dos niveles complementarios:

### Validación teórica (correctitud algorítmica)

Se implementa una validación exacta alternativa basada en recursión con memoización (denominada "brute force"), que calcula el número máximo de emparejamientos posibles.

- Se aplica únicamente sobre secuencias cortas debido a su coste computacional.
- Permite verificar que el algoritmo de Nussinov alcanza el óptimo global.
- La validación se basa en comparar el número de pares, ya que pueden existir múltiples estructuras óptimas equivalentes.

Esto garantiza la **correctitud de la implementación** desde el punto de vista algorítmico.

---

### Validación empírica (comportamiento en datos reales)

Se utiliza el dataset **bpRNA**, que contiene estructuras secundarias reales de RNA en formato dot-bracket.

- Se compara el número de emparejamientos predicho por Nussinov con el del dataset.
- Se calcula el error en número de pares.
- Se analiza el comportamiento del algoritmo en función de la longitud de la secuencia.

Este análisis permite evaluar hasta qué punto el modelo simplificado de Nussinov se aproxima a estructuras biológicamente reales.

---

## Referencia adicional: ViennaRNA

Como comparación adicional, se utiliza la librería **ViennaRNA**, que predice estructuras secundarias mediante la minimización de la energía libre (modelo termodinámico).

⚠️ Es importante destacar que:

- ViennaRNA **no se utiliza para validar la correctitud del algoritmo**.
- Su objetivo es servir como referencia biológica más realista.
- No se espera coincidencia exacta con Nussinov, ya que ambos optimizan criterios distintos.

---

## Conclusión metodológica

La combinación de validación teórica y empírica permite:

- Garantizar que la implementación es correcta (brute force)
- Evaluar su comportamiento en datos reales (bpRNA)
- Compararlo con un modelo biológico más avanzado (ViennaRNA)

Este enfoque proporciona un análisis completo tanto desde el punto de vista algorítmico como aplicado.

------------------------------------------------------------------------

## Funcionalidades

- Lectura de secuencias en formato FASTA
- Implementación propia del algoritmo de Nussinov
- Reconstrucción de la estructura secundaria mediante traceback
- Representación de la estructura en formato dot-bracket
- Validación exacta en secuencias cortas mediante brute force con memoización
- Comparación con estructuras reales del dataset bpRNA
- Benchmark reproducible y cálculo de métricas cuantitativas
- Generación automática de resultados, figuras y matrices
- Interfaz web interactiva desarrollada con Flask

------------------------------------------------------------------------

##  Estructura del proyecto

    Bioinformatica-proyecto/
    ├── src/
    │   ├── bruteforce.py
    │   ├── experiments.py
    │   ├── fasta_parser.py
    │   ├── main.py (Script sencillo para pruebas rápidas del algoritmo. NO PARA EXPERIMENTOS PRINCIPAL)
    │   ├── nussinov.py
    │   ├── scoring.py
    │   ├── traceback_nussinov.py
    │   └── utils.py
    │
    ├── scripts/
    │   └── filtrar_dbn.py
    │
    ├── data/
    │   ├── raw/
    │   │   ├── dbnFiles/
    │   │   ├── fastaFiles/
    │   │   └── ejemplo.fasta
    │   │
    │   └── processed/
    │       └── dbnFiles/
    │           ├── dataset.dbn
    │           └── dataset.fasta
    │
    ├── results/
    │   ├── resultados.csv
    │   ├── figures/
    │   ├── matrices/
    │   └── metrics/
    │       └── log.txt
    │
    ├── docs/
    │   └── analysis.ipynb
    │
    ├── templates/
    │   └── index.html
    │
    ├── static/
    │
    ├── tests/
    │   ├── test_fasta_parser.py
    │   ├── test_nussinov.py
    │   ├── test_scoring.py
    │   ├── test_traceback.py
    │   └── test_utils.py
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── README_final.md
    ├── pytest.ini
    └── LICENSE

------------------------------------------------------------------------

## Ejecución

A continuación se describen los pasos necesarios para ejecutar completamente el proyecto de forma reproducible.

---

### 1. Instalar dependencias

Instalar todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

En caso de no tener ViennaRNA instalado:

```bash
pip install ViennaRNA
```

### 2. Descargar y preparar el dataset

Este proyecto utiliza datos reales del dataset bpRNA.

- **Descargar dataset**

Descargar los archivos en formato .dbn desde:

https://bprna.cgrb.oregonstate.edu/download.php

- **Colocar archivos**

Mover todos los archivos descargados a:  

```bash
data/raw/dbnFiles
```

### 3. Generar dataset procesado

Ejecutar el script de filtrado:

```bash
    python scripts/filtrar_dbn.py
```

Este script:

•	filtra secuencias con longitud ≤ 120 nucleótidos

•	elimina estructuras con pseudonudos

•	genera:

```bash
data/processed/dbnFiles/dataset.dbn
data/processed/dbnFiles/dataset.fasta
```

### 4. Ejecutar experimentos

Ejecutar el benchmark completo:

```bash
    python -m src.experiments
```

Este proceso:

•	aplica Nussinov a todas las secuencias

•	compara con estructuras reales (DBN)

•	valida con brute force en secuencias cortas

•	mide tiempos de ejecución

Resultados generados en:

```bash
results/resultados.csv
results/metrics/log.txt
```

### 5. Análisis de resultados

Abrir:

    docs/analysis.ipynb

Incluye:

•	métricas cuantitativas  
•	visualización de resultados  
•	interpretación  
    
### 6. Web

Ejecutar: 

    python app.py

Abrir en navegador:

    http://127.0.0.1:5000

Permite:  
•	introducir secuencias  
•	visualizar estructuras  
•	comparar resultados  

---
⚠️ Notas importantes

- Usar ejecución como módulo:

    python -m src.experiments

- El proyecto es completamente reproducible siguiendo estos pasos

------------------------------------------------------------------------
## Benchmark

Se evalúa el comportamiento del algoritmo mediante:

- Tiempo de ejecución en función de la longitud
- Error absoluto respecto a estructuras reales (DBN)
- Error relativo en número de emparejamientos
- Validación exacta con brute force en secuencias cortas

Resultados disponibles en:

    results/resultados.csv

------------------------------------------------------------------------

## Resultados clave

- Nussinov es correcto desde el punto de vista algorítmico (validación exacta)
- Tiende a sobreestimar el número de emparejamientos
- El error aumenta con la longitud de la secuencia
- El tiempo de ejecución crece de forma coherente con O(n³)

------------------------------------------------------------------------

## ⚠️ Limitaciones

- Nussinov no considera energía ni estabilidad termodinámica
- No soporta pseudonudos []
- Sobreestima emparejamientos frente a estructuras reales
- Complejidad cúbica (O(n³))
- Validación exacta limitada a secuencias cortas

------------------------------------------------------------------------

## Conclusión

El algoritmo de Nussinov es correcto y eficiente desde el punto de vista computacional, pero presenta limitaciones importantes como modelo biológico, ya que no reproduce fielmente las estructuras reales del RNA.

Esto demuestra que maximizar el número de emparejamientos no es suficiente para modelar la estructura secundaria en contextos reales.

------------------------------------------------------------------------

## Reproducibilidad

El experimento completo puede reproducirse ejecutando:

```bash
python scripts/filtrar_dbn.py
python -m src.experiments
```
------------------------------------------------------------------------

## 📥 Formato de entrada


Ejemplo de archivo FASTA:

```bash
>secuencia_1
GGGAAAUCC
>secuencia_2
GGGGAAAACCCC
```

---


## 📤 Ejemplo de salida log

```bash
===================================
Secuencia: bpRNA_RFAM_14392
Longitud: 112

Nussinov → 44 pares
DBN → 20 pares
Error DBN: 24

BruteForce → 44
Coincide óptimo: True

Tiempo: 0.03701 s
===================================
```

---

## Diferencias entre modelos

- **Nussinov**: maximiza el número de emparejamientos mediante programación dinámica  
- **Brute force (con memoización)**: calcula la solución óptima exacta (solo en secuencias cortas)  
- **ViennaRNA**: minimiza la energía libre (modelo termodinámico)

Por ello:

- Nussinov y brute force deben coincidir en el número máximo de pares → validación de correctitud  
- ViennaRNA puede producir estructuras distintas → referencia biológica, no validación  

Esto refleja que maximizar emparejamientos no es equivalente a obtener estructuras biológicamente realistas.