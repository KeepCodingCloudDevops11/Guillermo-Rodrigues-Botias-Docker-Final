# GuillermoRodrigues-Docker-final
Práctica final módulo Docker Guillermo Rodrigues Botias

## INDICE

* [*Primera parte*](#primera-parte) : Objetio y Requisitos
* [*Segunda parte*](#segunda-parte) : Estrcutura y creación de contenedor Flask
* [*Tercera parte*](#tercera-parte) : Contenedor Base de Datos

 ## Primera Parte

 En esta práctica vamos a levantar dos contenedores de docker comunicados entre si, uno será flask y el otro mysql, tendremos un contador  persistente para que aunque paremos el contenedor, al volverlo a iniciar nos cuente desde donde lo paramos.

 Para conseguirlo necesitaremos:
 *Docker, Docker desktop
 *Docker compose para que lo levante y gestione automaticamente
 *Flask

 ## Segunda Parte

 En primer lugar, vamos a crear un repositorio en nuestro terminal, desde ahí comencaremos a trabajar, desde la raíz. Tendremos que crear archivos y carpteas con esta **estructura**, este es un ejemplo:

* 2.1 Estructura
 Guillermo-Rodrigues-Botias-Docker-Final/
     app/
         app.py           # Archivo principal de la aplicación
         requirements.txt # Dependencias de Python
         counter.txt      # Archivo de conteo
     docker-compose.yml   # Archivo de configuración de Docker Compose
     Dockerfile           # Archivo para construir la imagen Docker
     init.sql             # Archivo base de datos
     README.md            # Archivo de instrucciones

-En el archivo **app.py** añadimos el siguiente código

```bash
from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Ruta donde se almacenará el contador
COUNTER_FILE = "counter.txt"

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
```    
[Construcción de contenedor](https://github.com/KeepCodingCloudDevops11/Guillermo-Rodrigues-Botias-Docker-Final/blob/main/images/Construccion%20Flask%201.png)
[Flask levantado](https://github.com/KeepCodingCloudDevops11/Guillermo-Rodrigues-Botias-Docker-Final/blob/main/images/Flask%20levantado.png)

* 2.3 Añadimos ```flask``` al archivo requirements.txt

* 2.4 el archivo **Dockerfile** debe contener lo siguiente:

```bash
# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY app/ /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

```

* 2.5 Vamos ahora a configurar **docker-compose.yml** añadiendo al archivo el siguiente texto:

```bash
version: "3.8"

services:
  app:
    build:
      context: .
    ports:
      - "5000:5000"
    volumes:
      - ./app/counter.txt:/app/counter.txt
    restart: always

  db:
    image: mysql:8.0
    container_name: recambios_db
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: recambios
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  db_data:

```

* 2.6 El archivo dentro del directorio app llamado **counter.txt** lo tendremos vacio, en el se irá haciendo el conteo de las veces que nos hemos conectado.

## Tercera Parte

* 3.1 A continucaión vamos a crear el contenedor de la base de datos, para ello el archivo **init.sql** debe tener este código:

```bash
USE recambios;

CREATE TABLE IF NOT EXISTS piezas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

INSERT INTO piezas (nombre, descripcion, precio) VALUES
('Bloque de motor', 'Parte principal del motor que contiene los cilindros.', 1200.00),
('Culata', 'Parte superior del motor que sella los cilindros.', 800.00),
('Embrague', 'Permite la conexión y desconexión del motor y la transmisión.', 300.00);

```

* * 3.2 Con estos archivos ya creados vamos a levantar los contenedores usaremos docker-compose ya que nos falicitará la creacación de redes y demás, códigos en el mismo orden y siempre desde la raíz del proyecto:

* ```docker-compose build``` para construir la imagen del contenedor
* ```docker-compose up``` para iniciar el contenedor
* ```docker-compose down``` En el caso de tener que pararlos usaremos este código.
**Importante** cada modificaón que se haga en los archivos y para que se vean reflejados en la aplicaón, es necesario que se pare y vuelvan a construir.

* 3.4 Una vez construidos, probaremos la aplicación accediendo a ella desde nuestro navegador con **localhost:5000** y deberíamos ver algo como esto:
[Aplicacion terminada y funcionando](https://github.com/KeepCodingCloudDevops11/Guillermo-Rodrigues-Botias-Docker-Final/blob/main/images/Aplicaion%20funcionando.png)