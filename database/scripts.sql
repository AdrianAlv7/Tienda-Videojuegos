-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS activelife_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE activelife_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'cliente') NOT NULL DEFAULT 'cliente',
    edad INT DEFAULT NULL,
    altura DECIMAL(4,2) DEFAULT NULL,
    peso DECIMAL(5,2) DEFAULT NULL,
    objetivo VARCHAR(255) DEFAULT NULL,
    activo TINYINT(1) DEFAULT 1
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,   -- Agregado
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- Tabla de ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de detalle_ventas
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Inserta usuarios (contraseñas ya hasheadas)
INSERT INTO usuarios (username, email, password, role)
VALUES
  ('admin', 'admin@correo.com', 'scrypt:32768:8:1$lDiShujSp5jhis1t$f0ae7b554669c2f5b521f946d8845262bcd3269b12b4c0688eebf0b6b4db63c2649eba864c0b49045e47a3743c457fa69ecceec0875819caa93a72ce2706cd7e', 'admin'),
  ('editor', 'editor@correo.com', 'scrypt:32768:8:1$leQ3Jm7aGRPLGFGp$f2a71b0ea227d3b7a6898d28cda227db47d35f6e7721c39c30b5a204239e66a464fc5e24367cc390014e96e2c7297b5f6e51f86f50bcf84b70bcb202841f36db', 'editor'),
  ('cliente', 'cliente@correo.com', 'scrypt:32768:8:1$ynpKs2n4YfAkrX9K$ba5396b0d3c2d4b7f4c3c50e12b6d6ebf045ca81c88a48cc9ef0ea652f258f32d6d4f51a6dc7794d1b929a5c13e65b34a265c8afcdebfce3c35c0dfac7e32a49', 'cliente');

-- Inserta productos con categoría (sin imágenes)
INSERT INTO productos (nombre, descripcion, categoria, precio, stock) VALUES
  -- Rutinas de Ejercicio
  ('30 days Muscle Building', 'Rutina intensa para ganar músculo en 30 días.', 'rutina', 20.00, 50),
  ('Insanity Deluxe Edition', 'Entrenamiento avanzado de alta intensidad.', 'rutina', 25.00, 40),
  ('Fast Hiking', 'Programa para mejorar tu resistencia en senderismo.', 'rutina', 15.00, 60),
  -- Recetas Saludables
  ('Meal Menu for Hiking', 'Menú nutricional pensado para largas caminatas.', 'receta', 10.00, 30),
  ('50 Recetas para una Vida Saludable', 'Recetario para mejorar tu alimentación diaria.', 'receta', 12.00, 35),
  ('Recetario Semanal para Volumen', 'Recetas para ganar masa muscular de forma saludable.', 'receta', 18.00, 25);


CREATE TABLE juegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    imagen VARCHAR(255)
);
ALTER TABLE productos
ADD COLUMN imagen VARCHAR(255) AFTER descripcion;

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen VARCHAR(255),
    categoria VARCHAR(100),
    precio DECIMAL(10,2),
);


-- Tabla de usuarios (si no la tienes)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- Tabla de ventas (registro de compras)
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

-- Detalle de cada venta (qué productos se compraron)
CREATE TABLE detalle_venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);


CREATE TABLE coleccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    fecha_adquirido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);

-----------------------------------------
-- =====================================
-- 🎮 Base de datos: ActiveLife_DB (versión tienda videojuegos)
-- =====================================

CREATE DATABASE IF NOT EXISTS activelife_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE activelife_db;

-- =====================================
-- 🧍 Tabla de Usuarios
-- =====================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'cliente') NOT NULL DEFAULT 'cliente',
    edad INT DEFAULT NULL,
    altura DECIMAL(4,2) DEFAULT NULL,
    peso DECIMAL(5,2) DEFAULT NULL,
    objetivo VARCHAR(255) DEFAULT NULL,
    activo TINYINT(1) DEFAULT 1
);

-- =====================================
-- 🕹️ Tabla de Productos (Videojuegos)
-- =====================================
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen VARCHAR(255),  -- Nombre del archivo de imagen guardado en /static/IMG/
    precio DECIMAL(10,2) NOT NULL
);

-- =====================================
-- 💳 Tabla de Ventas (registro general)
-- =====================================
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- =====================================
-- 📦 Tabla de Detalle de Venta (qué se compró)
-- =====================================
CREATE TABLE IF NOT EXISTS detalle_venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);

-- =====================================
-- 📚 Tabla de Colección del Usuario (Biblioteca)
-- =====================================
CREATE TABLE IF NOT EXISTS coleccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    fecha_adquirido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE,
    UNIQUE (id_usuario, id_producto)  -- Evita duplicar juegos en la colección
);

-- =====================================
-- 👤 Usuarios iniciales
-- =====================================
INSERT INTO usuarios (username, email, password, role) VALUES
  ('admin', 'admin@correo.com', 'scrypt:32768:8:1$lDiShujSp5jhis1t$f0ae7b554669c2f5b521f946d8845262bcd3269b12b4c0688eebf0b6b4db63c2649eba864c0b49045e47a3743c457fa69ecceec0875819caa93a72ce2706cd7e', 'admin'),
  ('editor', 'editor@correo.com', 'scrypt:32768:8:1$leQ3Jm7aGRPLGFGp$f2a71b0ea227d3b7a6898d28cda227db47d35f6e7721c39c30b5a204239e66a464fc5e24367cc390014e96e2c7297b5f6e51f86f50bcf84b70bcb202841f36db', 'editor'),
  ('cliente', 'cliente@correo.com', 'scrypt:32768:8:1$ynpKs2n4YfAkrX9K$ba5396b0d3c2d4b7f4c3c50e12b6d6ebf045ca81c88a48cc9ef0ea652f258f32d6d4f51a6dc7794d1b929a5c13e65b34a265c8afcdebfce3c35c0dfac7e32a49', 'cliente');

-- 🎮 Insertar videojuegos de ejemplo (sin imagen, usa default)
INSERT INTO productos (nombre, descripcion, imagen, precio) VALUES
('Juego 1', 'Un emocionante juego de acción lleno de aventura.', NULL, 19.99),
('Juego 2', 'Explora mundos abiertos y enfrenta desafíos épicos.', NULL, 24.99),
('Juego 3', 'Rompecabezas con una historia envolvente y misteriosa.', NULL, 14.99),
('Juego 4', 'Simulador de estrategia con múltiples modos de juego.', NULL, 29.99),
('Juego 5', 'Un clásico juego de plataformas rediseñado para hoy.', NULL, 9.99);


-- 🔧 Crear tabla de ventas (si no existe)
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- 🔧 Crear tabla de detalle de ventas (qué productos compró cada usuario)
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- 🔧 Crear tabla de biblioteca (colección de juegos del usuario)
CREATE TABLE IF NOT EXISTS biblioteca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    fecha_adquirido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);


ALTER TABLE usuarios
DROP COLUMN edad,
DROP COLUMN altura,
DROP COLUMN peso,
DROP COLUMN objetivo;

ALTER TABLE usuarios
ADD COLUMN foto_perfil VARCHAR(255) DEFAULT NULL AFTER role,
ADD COLUMN banner VARCHAR(255) DEFAULT NULL AFTER foto_perfil,
ADD COLUMN tema ENUM('oscuro','claro') DEFAULT 'oscuro' AFTER banner,
ADD COLUMN descripcion TEXT DEFAULT NULL AFTER tema;

ALTER TABLE usuarios ADD COLUMN tema ENUM('oscuro', 'claro') DEFAULT 'oscuro';

ALTER TABLE usuarios DROP COLUMN tema;

CREATE TABLE IF NOT EXISTS imagenes_producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    nombre_imagen VARCHAR(255) NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS carrito (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_usuario_producto (id_usuario, id_producto),
  CONSTRAINT fk_carrito_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
  CONSTRAINT fk_carrito_producto FOREIGN KEY (id_producto) REFERENCES productos(id)
);

ALTER TABLE carrito MODIFY cantidad INT DEFAULT 1;


ALTER TABLE carrito ADD UNIQUE KEY unq_usuario_producto (id_usuario, id_producto);
