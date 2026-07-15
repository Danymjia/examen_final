from flask import Flask, render_template, request, redirect, Response
import mysql.connector
import os
import json

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="mysql_principal",
        user="root",
        password="root",
        database="examenad"
    )

@app.route("/")
def index():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, accion, fecha, hora, short FROM redes ORDER BY id DESC LIMIT 15")
        rows = cursor.fetchall()
        conn.close()
        db_status = "Conectado"
        
        redes = []
        for r in rows:
            redes.append({
                "id": r[0],
                "usuario": r[1],
                "accion": r[2],
                "fecha_str": str(r[3]),
                "hora_str": str(r[4]),
                "short": r[5]
            })
    except Exception as e:
        redes = []
        db_status = f"Error: {e}"

    metrics = None
    for path in ["shared/resultados.json", "resultados.json"]:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    metrics = json.load(f)
                break
            except Exception:
                pass

    return render_template(
        "index.html",
        server_name="Servidor 1",
        db_status=db_status,
        redes=redes,
        metrics=metrics
    )

@app.route("/agregar", methods=["POST"])
def agregar():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO redes (usuario, accion, fecha, hora, short) VALUES (%s, %s, %s, %s, %s)",
            (request.form["usuario"], request.form["accion"], request.form["fecha"], request.form["hora"], request.form["short"])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error insert: {e}")
    return redirect("/")

@app.route("/datos")
def datos():
    print("Request for /datos handled by Servidor 1", flush=True)
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, accion, fecha, hora, short FROM redes")
        rows = cursor.fetchall()
        conn.close()
        
        lines = [f"{r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]}" for r in rows]
        return Response("\n".join(lines), mimetype="text/plain")
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)