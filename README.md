# Bioinformatica-proyecto

## Predicción de estructura secundaria de RNA con Nussinov

Este proyecto implementa el algoritmo de **Nussinov** para predecir estructura secundaria de RNA mediante programación dinámica. La implementación mantiene el esquema clásico **O(n^3)** y añade dos restricciones sencillas para acercarse algo más al comportamiento estructural real:

- **longitud mínima de loop** (`min_loop_length = 3`)
- **penalización de loops largos** (`long_loop_penalty = 0.25` a partir de `long_loop_threshold = 30`)

Además del cálculo de la matriz óptima, el proyecto incluye:

- reconstrucción por `traceback`
- conversión a formato dot-bracket
- visualización web sencilla con Flask
- validación exacta alternativa en secuencias cortas mediante búsqueda recursiva con memoización
- comparación experimental con estructuras reales de **bpRNA**
- comparación de referencia con **ViennaRNA / RNAfold**

## Estructura

```text
Bioinformatica-proyecto/
├── app.py
├── requirements.txt
├── README.md
├── scripts/
│   └── filtrar_dbn.py
├── src/
│   ├── bruteforce.py
│   ├── experiments.py
│   ├── fasta_parser.py
│   ├── main.py
│   ├── nussinov.py
│   ├── scoring.py
│   ├── traceback_nussinov.py
│   └── utils.py
├── templates/
│   └── index.html
├── tests/
│   ├── test_fasta_parser.py
│   ├── test_nussinov.py
│   ├── test_scoring.py
│   ├── test_traceback.py
│   └── test_utils.py
└── results/
```

## Dataset

El dataset **no está subido al repositorio** porque su tamaño es demasiado grande para incluirlo de forma razonable. 

Fuente recomendada:

- [bpRNA download](https://bprna.cgrb.oregonstate.edu/download.php)

### Ubicación esperada

Para que el origen de cada archivo quede claro, la organización recomendada es esta:

- `data/raw/dataset_download/`: datos descargados externamente de bpRNA
- `data/raw/web_inputs/`: ejemplos manuales y FASTA subidos desde la app web

Descarga los archivos `.dbn` y colócalos en:

```bash
data/raw/dataset_download/dbnFiles
```

Si también conservas FASTA descargados del dataset, guárdalos en:

```bash
data/raw/dataset_download/fastaFiles
```

Los FASTA de ejemplo para probar la app o la demo por terminal pueden ir en:

```bash
data/raw/web_inputs/examples
```

Los FASTA subidos desde la interfaz web se guardan automáticamente en:

```bash
data/raw/web_inputs/uploads
```

Después ejecuta:

```bash
python3 scripts/filtrar_dbn.py
```

Ese script:

- filtra secuencias de longitud `<= 120`
- elimina entradas con pseudonudos simples (`[` y `]`)
- genera:

```bash
data/processed/dbnFiles/dataset.dbn
data/processed/dbnFiles/dataset.fasta
```

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si no quieres usar la comparación con ViennaRNA, el núcleo algorítmico sigue funcionando aunque esa librería no esté disponible. La comparación con `RNA.fold` pasará a mostrarse como no disponible.

## Ejecución rápida

### Demo por terminal

```bash
python3 -m src.main
```

Ese script lee por defecto:

```bash
data/raw/web_inputs/examples/ejemplo.fasta
```

### Interfaz web

```bash
python3 app.py
```

Abre [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Experimentos

Con el dataset procesado ya generado:

```bash
python3 -m src.experiments
```

Se generan automáticamente:

- `results/resultados.csv`
- `results/metrics/log.txt`
- `results/metrics/fallo_estructural.txt`
- `results/figures/tiempo_vs_longitud.png`
- `results/figures/error_vs_longitud.png`
- `results/figures/comparacion_pares.png`
- `results/figures/comparacion_viennarna.png` si ViennaRNA está disponible

## Qué hace exactamente el modelo

La recurrencia sigue la idea clásica de Nussinov: para cada subsecuencia `(i, j)` se evalúan estas opciones:

1. dejar `i` sin emparejar
2. dejar `j` sin emparejar
3. emparejar `i` con `j` si el par es válido
4. dividir el problema en dos subproblemas

La complejidad temporal es **O(n^3)** por el recorrido de diagonales y el barrido de particiones `k`. El espacio es **O(n^2)** por la matriz dinámica.

En esta versión, un par solo se admite si:

- es válido (`A-U`, `U-A`, `G-C`, `C-G`)
- respeta una longitud mínima de loop

Además, si el loop inducido es demasiado largo, se reduce ligeramente su score. El objetivo deja de ser “maximizar solo el número bruto de pares” y pasa a ser “maximizar una puntuación estructural simple”.

## Validación y benchmarks

El proyecto evalúa el algoritmo en tres niveles:

- **correctitud interna**: comparación con un resolvedor exacto alternativo en secuencias cortas
- **comparación con bpRNA**: número de pares predichos frente a la estructura anotada real
- **comparación con ViennaRNA / RNAfold**: referencia termodinámica externa

También se incluye un pequeño **test de fallo estructural** en `results/metrics/fallo_estructural.txt` para dejar documentado que maximizar pares no equivale a modelar bien la estructura biológica real.

## Tests

```bash
python3 -m pytest -q
```

## Reproducibilidad

Para reproducir el proyecto hace falta:

- clonar el repositorio
- instalar dependencias
- descargar bpRNA manualmente
- ejecutar `scripts/filtrar_dbn.py`
- lanzar `src.experiments`

La descarga manual del dataset es el único paso externo importante, y se mantiene fuera del repositorio por tamaño.
