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
