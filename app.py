from flask import Flask, render_template, request
import RNA

from src.nussinov import nussinov
from src.traceback_nussinov import traceback
from src.utils import pares_a_dot_bracket
from src.fasta_parser import leer_fasta
from src.bruteforce import max_pares_fuerza_bruta

app = Flask(__name__)


def ejecutar_viennarna(secuencia):
    estructura, energia = RNA.fold(secuencia)
    return estructura, energia


def procesar_secuencia(secuencia):
    secuencia = secuencia.strip().upper().replace("T", "U")

    if not secuencia:
        return {"error": "La secuencia está vacía."}

    caracteres_validos = {"A", "U", "G", "C"}
    if any(base not in caracteres_validos for base in secuencia):
        return {"error": "La secuencia contiene caracteres no válidos. Usa solo A, U, G y C."}

    matriz = nussinov(secuencia)
    pares = traceback(matriz, secuencia, 0, len(secuencia) - 1, [])
    estructura_nussinov = pares_a_dot_bracket(len(secuencia), pares)
    num_pares = matriz[0][len(secuencia) - 1] if secuencia else 0

    estructura_vienna, energia = ejecutar_viennarna(secuencia)

    # Validación exacta por fuerza bruta solo para secuencias cortas
    resultado_bruteforce = None
    if len(secuencia) <= 14:
        max_bruto, pares_bruto = max_pares_fuerza_bruta(secuencia)
        estructura_bruta = pares_a_dot_bracket(len(secuencia), pares_bruto)

        resultado_bruteforce = {
            "max_pares": max_bruto,
            "pares": pares_bruto,
            "estructura": estructura_bruta,
            "coincide": max_bruto == num_pares
        }

    return {
        "secuencia": secuencia,
        "estructura_nussinov": estructura_nussinov,
        "estructura_vienna": estructura_vienna,
        "energia": energia,
        "pares": pares,
        "num_pares": num_pares,
        "bruteforce": resultado_bruteforce,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    error = None

    if request.method == "POST":
        secuencia_manual = request.form.get("secuencia", "").strip()
        archivo = request.files.get("fasta")

        if secuencia_manual:
            resultado = procesar_secuencia(secuencia_manual)
            if "error" in resultado:
                error = resultado["error"]
            else:
                resultados.append(resultado)

        elif archivo and archivo.filename:
            ruta_temp = "temp_input.fasta"
            archivo.save(ruta_temp)

            try:
                secuencias = leer_fasta(ruta_temp)
                for secuencia in secuencias:
                    resultado = procesar_secuencia(secuencia)
                    if "error" in resultado:
                        error = resultado["error"]
                        break
                    resultados.append(resultado)
            except Exception as e:
                error = f"Error al leer el archivo FASTA: {e}"

        else:
            error = "Introduce una secuencia o sube un archivo FASTA."

    return render_template("index.html", resultados=resultados, error=error)


if __name__ == "__main__":
    app.run(debug=True)