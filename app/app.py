from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Ruta del contador desde la variable de entorno
COUNTER_FILE = os.getenv("COUNTER_FILE", "counter.txt")  # Valor por defecto


def get_counter():
    if not os.path.exists(COUNTER_FILE) or os.path.getsize(COUNTER_FILE) == 0:
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    with open(COUNTER_FILE, "r") as f:
        return int(f.read())

def increment_counter():
    count = get_counter() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))
    return count

@app.route("/")
def index():
    count = increment_counter()
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contador y Base de Datos</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            h1 { color: #333; }
            table { margin: 20px auto; border-collapse: collapse; width: 60%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f4f4f4; }
            footer {
                text-align: left;
                font-size: 12px;
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color : #f1f11f1;
                padding: 10px;
            }    
        </style>
    </head>
    <body>
        <h1>Aplicación Flask con Base de datos y Contador</h1>
        <p>Esta página ha sido visitada <strong>{{ count }}</strong> veces.</p>
        <h2>Conexión con la Base de Datos</h2>
        <p>La base de datos contendrá las siguientes piezas:</p>
        <table>
            <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Precio (€)</th>
            </tr>
            <tr>
                <td>Bloque de motor</td>
                <td>Parte principal del motor que contiene los cilindros.</td>
                <td>1200.00</td>
            </tr>
            <tr>
                <td>Culata</td>
                <td>Parte superior del motor que sella los cilindros.</td>
                <td>800.00</td>
            </tr>
            <tr>
                <td>Embrague</td>
                <td>Permite la conexión y desconexión del motor y la transmisión.</td>
                <td>300.00</td>
            </tr>
        </table>

        <footer>Práctica Docker Guillermo Rodrigues Botias</footer>
    </body>
    </html>
    """
    return render_template_string(html_content, count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
