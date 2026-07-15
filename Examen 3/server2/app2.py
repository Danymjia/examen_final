from flask import Flask, render_template, request, redirect, Response, jsonify
import mysql.connector
import datetime
import os
import json

app = Flask(__name__)

conexion = None

def get_db_connection():
    global conexion
    if conexion is None:
        try:
            conexion = mysql.connector.connect(
                host="mysql_principal",
                user="root",
                password="root",
                database="examenad"
            )
        except Exception as e:
            print(f"Error: {e}", flush=True)
    
@app.route("/")
def index():
    server_name = "Servidor 2"
    db_status = "Conectado"
    redes_data = []
    mapreduce_data = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, usuario, accion, fecha, hora, short FROM redes ORDER BY id DESC LIMIT 15")
        redes_data = cursor.fetchall()
        
        for row in redes_data:
            if isinstance(row['fecha'], (datetime.date, datetime.datetime)):
                row['fecha_str'] = row['fecha'].strftime('%Y-%m-%d')
            else:
                row['fecha_str'] = str(row['fecha'])
                
            if isinstance(row['hora'], datetime.timedelta):
                tot_sec = int(row['hora'].total_seconds())
                hours = tot_sec // 3600
                mins = (tot_sec % 3600) // 60
                secs = tot_sec % 60
                row['hora_str'] = f"{hours:02d}:{mins:02d}:{secs:02d}"
            elif isinstance(row['hora'], datetime.time):
                row['hora_str'] = row['hora'].strftime('%H:%M:%S')
            else:
                row['hora_str'] = str(row['hora'])
    except Exception as e:
        db_status = f"Error: {str(e)}"
        print(f"Index route DB error: {e}", flush=True)

    results_paths = ["/app/shared/resultados.json", "/app/resultados.json", "./resultados.json", "resultados.json"]
    for path in results_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    mapreduce_data = json.load(f)
                break
            except Exception as e:
                print(f"Error reading MapReduce results file at {path}: {e}", flush=True)

    return render_template(
        "index.html",
        server_name=server_name,
        db_status=db_status,
        redes=redes_data,
        metrics=mapreduce_data
    )

@app.route("/datos")
def datos():
    print("peticion datos servidor 2", flush=True)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usuario, accion, fecha, hora, short FROM redes")
        rows = cursor.fetchall()
        lines = []
        for row in rows:
            u = row['usuario']
            a = row['accion']
            f = row['fecha']
            h = row['hora']
            s = row['short']
            
            if isinstance(f, (datetime.date, datetime.datetime)):
                f_str = f.strftime('%Y-%m-%d')
            else:
                f_str = str(f)
            
            if isinstance(h, datetime.timedelta):
                tot_sec = int(h.total_seconds())
                hours = tot_sec // 3600
                mins = (tot_sec % 3600) // 60
                secs = tot_sec % 60
                h_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
            elif isinstance(h, datetime.time):
                h_str = h.strftime('%H:%M:%S')
            else:
                h_str = str(h)
            
            lines.append(f"{u}, {a}, {f_str}, {h_str}, {s}")
        
        response_text = "\n".join(lines)
        resp = Response(response_text, mimetype="text/plain")
        resp.headers["X-Served-By"] = "server2"
        return resp
    except Exception as e:
        return f"Error connecting to database: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)