from flask import Flask, render_template, request
from pathlib import Path
from uuid import uuid4

from src.nussinov import nussinov
from src.traceback_nussinov import traceback
from src.utils import ejecutar_viennarna, pares_a_dot_bracket
from src.fasta_parser import leer_fasta
from src.bruteforce import max_pares_fuerza_bruta

app = Flask(__name__)

UPLOAD_DIR = Path("data/raw/web_inputs/uploads")


def guardar_fasta_subido(archivo):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    nombre_original = Path(archivo.filename or "input.fasta").name
    nombre_limpio = nombre_original.replace(" ", "_")
    destino = UPLOAD_DIR / f"{uuid4().hex[:8]}_{nombre_limpio}"
    archivo.save(destino)
    return str(destino)


def procesar_secuencia(secuencia):
    secuencia = secuencia.strip().upper().replace("T", "U")

    if not secuencia:
        return {"error": "La secuencia está vacía."}

    if len(secuencia) > 300:
        return {"error": "Secuencia demasiado larga (máx 300 nucleótidos)"}

    if any(base not in {"A", "U", "G", "C"} for base in secuencia):
        return {"error": "Solo se permiten A, U, G, C"}

    #  NUSSINOV
    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura_nussinov = pares_a_dot_bracket(len(secuencia), pares)
    score_nussinov = matriz[0][len(secuencia) - 1]
    num_pares = len(pares)

    #  VIENNA (solo referencia)
    estructura_vienna, energia = ejecutar_viennarna(secuencia)
    num_pares_vienna = estructura_vienna.count("(") if estructura_vienna else None

    #  BRUTE FORCE (solo corto)
    resultado_bruteforce = None
    if len(secuencia) <= 120:
        score_bruto, pares_bruto = max_pares_fuerza_bruta(secuencia)
        estructura_bruta = pares_a_dot_bracket(len(secuencia), pares_bruto)

        resultado_bruteforce = {
            "score": score_bruto,
            "max_pares": len(pares_bruto),
            "pares": pares_bruto,
            "estructura": estructura_bruta,
            "coincide": abs(score_bruto - score_nussinov) <= 1e-9
        }

    return {
        "secuencia": secuencia,
        "estructura_nussinov": estructura_nussinov,
        "estructura_vienna": estructura_vienna,
        "energia": energia,
        "pares": pares,
        "num_pares": num_pares,
        "score_nussinov": score_nussinov,
        "bruteforce": resultado_bruteforce,
        "num_pares_vienna": num_pares_vienna,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    error = None

    if request.method == "POST":
        secuencia_manual = request.form.get("secuencia", "").strip()
        archivo = request.files.get("fasta")

        #  CASO 1 → input manual
        if secuencia_manual:
            resultado = procesar_secuencia(secuencia_manual)
            if "error" in resultado:
                error = resultado["error"]
            else:
                resultados.append(resultado)

        #  CASO 2 → archivo FASTA
        elif archivo and archivo.filename:
            ruta_temp = guardar_fasta_subido(archivo)

            try:
                secuencias = leer_fasta(ruta_temp)

                for nombre, secuencia in secuencias:   # 🔥 IMPORTANTE
                    resultado = procesar_secuencia(secuencia)

                    if "error" in resultado:
                        error = resultado["error"]
                        break

                    resultados.append(resultado)

            except Exception as e:
                error = f"Error leyendo FASTA: {e}"

        else:
            error = "Introduce una secuencia o sube un FASTA."

    return render_template("index.html", resultados=resultados, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
