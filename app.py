from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 🔹 Inicializar base de datos
def init_db():
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            fecha TEXT,
            hora TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# 🔹 Página principal
@app.route("/")
def index():
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM turnos ORDER BY fecha, hora")
    turnos = cursor.fetchall()

    conn.close()

    return render_template("index.html", turnos=turnos)


# 🔹 Agregar turno
@app.route("/agregar", methods=["POST"])
def agregar():
    cliente = request.form["cliente"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]

    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()

    # Evitar duplicados
    cursor.execute("SELECT * FROM turnos WHERE fecha=? AND hora=?", (fecha, hora))
    existente = cursor.fetchone()

    if existente:
        conn.close()
        return "⚠️ Ese horario ya está ocupado"

    cursor.execute(
        "INSERT INTO turnos (cliente, fecha, hora) VALUES (?, ?, ?)",
        (cliente, fecha, hora)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# 🔹 Eliminar turno
@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM turnos WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


# 🔹 Ejecutar app
if __name__ == "__main__":
    app.run(debug=True)