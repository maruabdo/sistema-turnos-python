from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ARCHIVO = "turnos.json"


def cargar_turnos():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


def guardar_turnos(turnos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(turnos, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    turnos = cargar_turnos()
    turnos = sorted(turnos, key=lambda x: (x["fecha"], x["hora"]))
    return render_template("index.html", turnos=turnos)


@app.route("/agregar", methods=["POST"])
def agregar():
    cliente = request.form["cliente"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]

    turnos = cargar_turnos()

    # evitar duplicados
    for t in turnos:
        if t["fecha"] == fecha and t["hora"] == hora:
            return "Ese horario ya está ocupado"

    turnos.append({
        "cliente": cliente,
        "fecha": fecha,
        "hora": hora
    })

    guardar_turnos(turnos)
    return redirect("/")


@app.route("/eliminar/<int:index>")
def eliminar(index):
    turnos = cargar_turnos()
    if 0 <= index < len(turnos):
        turnos.pop(index)
        guardar_turnos(turnos)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
    