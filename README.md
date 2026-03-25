# Bioinformatica-proyecto

# Predicción de estructura secundaria de RNA con el algoritmo de Nussinov

## Objetivo
Desarrollar una herramienta en Python que reciba una secuencia de RNA y prediga su estructura secundaria óptima mediante el algoritmo de Nussinov.

## Funcionalidades previstas
- Lectura de secuencias en formato FASTA
- Implementación del algoritmo de Nussinov
- Reconstrucción de la estructura secundaria óptima
- Evaluación experimental del rendimiento
- Posibles extensiones: penalización de loops cortos y visualización simple

## Estructura del proyecto
- `src/`: código fuente
- `data/`: datos de entrada
- `tests/`: pruebas
- `results/`: resultados y salidas

## Cómo ejecutar
```bash
python src/main.py

## Autoras
	•	Laura Pérez López
	•	Gloria Díaz Jiménez
	•	Isabel Roldán Barros

---

## 5. Crea las primeras issues en GitHub
Esto os va a ordenar muchísimo. Por ejemplo:

- `#1 Crear estructura inicial del repositorio`
- `#2 Implementar parser FASTA`
- `#3 Implementar matriz DP del algoritmo de Nussinov`
- `#4 Implementar traceback`
- `#5 Diseñar casos de prueba pequeños`
- `#6 Añadir métricas de evaluación`
- `#7 Comparar con herramientas existentes`
- `#8 Generar visualización simple de la estructura`

Así cada una puede ir cogiendo tareas.

---

## 6. Repartid el trabajo con ramas
No trabajéis todas sobre `main`.

Haced algo así:
- `main` → versión estable
- `dev` → integración
- ramas individuales:
  - `feature/fasta-parser`
  - `feature/nussinov-core`
  - `feature/traceback`
  - `feature/evaluation`

Flujo simple:
1. crear rama
2. trabajar ahí
3. hacer commit
4. push
5. abrir Pull Request
6. otra compañera revisa
7. merge a `dev` o `main`

---

## 7. Empieza por un prototipo mínimo
No intentéis hacer todo a la vez. El orden ideal sería:

### Fase 1
Leer una secuencia simple de RNA manualmente:
```python
seq = "GGGAAAUCC"