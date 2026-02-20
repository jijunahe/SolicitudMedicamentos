-- Ejecutar como root: sudo mysql < backend/scripts/otorgar_permisos_eps.sql
CREATE USER IF NOT EXISTS 'eps'@'localhost' IDENTIFIED BY '12345678';
CREATE USER IF NOT EXISTS 'eps'@'%' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON solicitud_medicamentos.* TO 'eps'@'localhost';
GRANT ALL PRIVILEGES ON solicitud_medicamentos.* TO 'eps'@'%';
FLUSH PRIVILEGES;
