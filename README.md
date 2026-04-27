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
├── LICENSE
├── pytest.ini
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
├── static/
│   └── rna_1.png
├── tests/
│   ├── test_fasta_parser.py
│   ├── test_nussinov.py
│   ├── test_scoring.py
│   ├── test_traceback.py
│   └── test_utils.py
├── docs/
│   └── analysis.ipynb
├── data/
│   ├── raw/
│   │   ├── dataset_download/
│   │   │   ├── dbnFiles/
│   │   │   └── fastaFiles/
│   │   └── web_inputs/
│   │       ├── examples/
│   │       └── uploads/
│   │           └── web/
│   └── processed/
│       └── dbnFiles/
│           ├── dataset.dbn
│           └── dataset.fasta
└── results/
    ├── figures/
    ├── matrices/
    ├── metrics/
    └── resultados.csv
```

### Estructura general

- `app.py`  
  Interfaz web en Flask para introducir secuencias o subir archivos FASTA y visualizar la predicción.

- `src/`  
  Núcleo del proyecto: implementación del algoritmo de Nussinov, reconstrucción de la estructura, utilidades y experimentos.

- `scripts/`  
  Scripts auxiliares para preparar el dataset antes de ejecutar los experimentos.

- `tests/`  
  Pruebas unitarias para comprobar el parser, el algoritmo, el traceback y funciones auxiliares.

- `data/raw/`  
  Datos en bruto, organizados por origen:
  - `dataset_download/`: archivos descargados externamente del dataset bpRNA.
  - `web_inputs/`: ejemplos manuales y archivos FASTA subidos desde la aplicación web.

- `data/processed/`  
  Datos ya filtrados y preparados para el benchmark experimental.

- `results/`  
  Resultados generados por los experimentos: métricas, matrices y figuras.

- `docs/`  
  Material de análisis y apoyo, como el cuaderno `analysis.ipynb`.

- `templates/` y `static/`  
  Recursos de la interfaz web.

## Dataset

El dataset **no está subido al repositorio** porque su tamaño es demasiado grande para incluirlo de forma razonable.

Fuente de descarga:

- [bpRNA download](https://bprna.cgrb.oregonstate.edu/download.php)

> Nota: durante la revisión final del proyecto, se observó que el enlace de descarga de bpRNA indicaba que el servidor estaba activo, pero la web no estaba correctamente desplegada (aparecía el mensaje de Apache por defecto). Esto sugiere un problema temporal del servicio. En cualquier caso, el proyecto puede ejecutarse igualmente utilizando los datos ya procesados (tras la ejecucion de scripts/filtrar_dbn.py) incluidos en `data/processed/`.

### Qué hay que descargar exactamente

Para reproducir este proyecto correctamente, no basta con descargar un único archivo.  
Desde la página de bpRNA deben descargarse **dos conjuntos de datos por separado**:

1. **Fasta Files**
2. **Dot-Bracket Files**

En la web de bpRNA aparecen como carpetas o paquetes separados para descarga.  
Una vez descargados y descomprimidos, deben colocarse ambas carpetas **tal cual** dentro de `data/raw/dataset_download/`, manteniendo sus nombres y su organización.

### Estructura esperada tras la descarga

Después de descomprimir ambos paquetes, la carpeta `data/raw/` debe quedar así:

```text
data/
└── raw/
    ├── dataset_download/
    │   ├── fastaFiles/
    │   └── dbnFiles/
    └── web_inputs/
        ├── examples/
        └── uploads/
            └── web/
```

## Crear y activar entorno virtual

Ejecutar los comandos desde la raíz del proyecto (`Bioinformatica-proyecto/`).

### Mac / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Windows (CMD)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En Mac/Linux puede ser necesario usar `python3` en lugar de `python`. Una vez activado el entorno virtual, normalmente puede usarse `python` en todos los comandos.

La comparación con ViennaRNA/RNAfold es opcional. Si no está disponible, el núcleo algorítmico del proyecto sigue funcionando y la comparación con `RNA.fold` pasará a mostrarse como no disponible.

## Ejecución rápida

### Demo por terminal

```bash
python -m src.main
```

Si el comando anterior no funciona en Mac/Linux, usar:

```bash
python3 -m src.main
```

### Interpretación de la salida

Al ejecutar el script principal, se muestra por consola un resumen por cada secuencia analizada. Un ejemplo es:

```
==============================
Secuencia: GGGAAAUCCGGAUCGGAUCGGCUAGCGGAUCGGAUCGGCUAGCGGAUCGGAU
Longitud: 52

Nussinov : .....(((((...))((((.((((((.(((...)))).)))))).)))).))
Pares Nussinov: 18
Score Nussinov: 17.00
BruteForce pares: 17
BruteForce score: 17.00
Coincide óptimo: True

ViennaRNA: .((....))..(((.((((.((((((.(((...))).)))))).)))).)))
Energía ViennaRNA: -24.20
==============================
```

Cada campo representa:

- **Secuencia**: identificador o cadena de RNA analizada.
- **Longitud**: número de nucleótidos.

- **Nussinov**: estructura predicha en formato *dot-bracket*.
- **Pares Nussinov**: número total de pares de bases predichos.
- **Score Nussinov**: valor de la función objetivo del algoritmo.

- **BruteForce pares / score**: resultado óptimo exacto calculado por fuerza bruta (solo para secuencias cortas).
- **Coincide óptimo**: indica si Nussinov alcanza el óptimo exacto.

- **ViennaRNA**: estructura predicha por RNAfold (modelo termodinámico).
- **Energía ViennaRNA**: energía libre asociada a esa estructura (más negativa → más estable).

Esto permite comparar directamente la predicción de Nussinov con una referencia exacta (fuerza bruta) y una referencia biológica (ViennaRNA).

### Interfaz web

```bash
python app.py
```

Si el comando anterior no funciona en Mac/Linux, usar:

```bash
python3 app.py
```

Al ejecutar el comando, debería aparecer un mensaje como:

Running on http://127.0.0.1:5000

Abrir esa URL en el navegador. 

> Nota: si el puerto 5000 está ocupado, Flask puede usar otro puerto (por ejemplo 5001). En ese caso, abrir la URL que aparezca en la terminal.

### Experimentos

```bash
python -m src.experiments
```

Si el comando anterior no funciona en Mac/Linux, usar:

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

- **correctitud interna**: comparación con un resolvedor exacto alternativo en secuencias cortas.
- **comparación con bpRNA**: número de pares predichos frente a la estructura anotada real en formato dot-bracket.
- **comparación con ViennaRNA / RNAfold**: referencia termodinámica externa para contrastar la predicción de Nussinov.

Para cada secuencia se registran métricas como la longitud, el score obtenido por Nussinov, el número de pares predichos, el error respecto a bpRNA, el error respecto a ViennaRNA y el tiempo de ejecución.

También se incluye un pequeño **test de fallo estructural** en `results/metrics/fallo_estructural.txt` para dejar documentado que maximizar pares no equivale necesariamente a modelar la estructura biológicamente o termodinámicamente más plausible.

## Tests

```bash
python -m pytest -q
```

Si el comando anterior no funciona en Mac/Linux, usar:

```bash
python3 -m pytest -q
```
