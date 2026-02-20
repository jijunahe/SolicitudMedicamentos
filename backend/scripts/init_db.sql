-- Script de creación de base de datos y tablas
-- MySQL - Solicitud de Medicamentos
-- Ejecutar como root: mysql -u root -p < backend/scripts/init_db.sql

CREATE DATABASE IF NOT EXISTS solicitud_medicamentos
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Usuario eps (si no existe) y permisos sobre la base de datos
CREATE USER IF NOT EXISTS 'eps'@'localhost' IDENTIFIED BY '12345678';
CREATE USER IF NOT EXISTS 'eps'@'%' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON solicitud_medicamentos.* TO 'eps'@'localhost';
GRANT ALL PRIVILEGES ON solicitud_medicamentos.* TO 'eps'@'%';
FLUSH PRIVILEGES;

USE solicitud_medicamentos;

-- Tabla usuarios (password almacenado encriptado en aplicación)
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  nombre VARCHAR(255) NULL,
  creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_email (email)
) ENGINE=InnoDB;

-- Tabla medicamentos (es_pos: 1 = POS, 0 = NO POS)
CREATE TABLE IF NOT EXISTS medicamentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  codigo VARCHAR(100) NULL UNIQUE,
  es_pos TINYINT(1) NOT NULL DEFAULT 1,
  creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_es_pos (es_pos)
) ENGINE=InnoDB;

-- Tabla solicitudes (campos NO POS opcionales en BD; validación en API)
CREATE TABLE IF NOT EXISTS solicitudes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  medicamento_id INT NOT NULL,
  es_no_pos TINYINT(1) NOT NULL DEFAULT 0,
  numero_orden VARCHAR(255) NULL,
  direccion TEXT NULL,
  telefono VARCHAR(50) NULL,
  correo VARCHAR(255) NULL,
  creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id) ON DELETE RESTRICT,
  INDEX idx_usuario (usuario_id),
  INDEX idx_creado (creado_en)
) ENGINE=InnoDB;

-- Datos iniciales: medicamentos de ejemplo (algunos POS, algunos NO POS)
INSERT INTO medicamentos (nombre, codigo, es_pos) VALUES
  ('Acetaminofén 500mg', 'ACET500', 1),
  ('Ibuprofeno 400mg', 'IBU400', 1),
  ('Omeprazol 20mg', 'OME20', 1),
  ('Medicamento NO POS A', 'NOPOS-A', 0),
  ('Medicamento NO POS B', 'NOPOS-B', 0);
