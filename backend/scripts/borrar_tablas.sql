-- Borra las tablas para poder probar de nuevo las semillas al arrancar el backend.
-- Ejecutar: mysql -u eps -p12345678 solicitud_medicamentos < backend/scripts/borrar_tablas.sql

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS solicitudes;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS medicamentos;
SET FOREIGN_KEY_CHECKS = 1;
