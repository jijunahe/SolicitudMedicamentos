# Modelo entidad-relación

Diagrama a nivel conceptual de las tablas y cómo se relacionan.

## Diagrama

```
+-------------+         +----------------+         +--------------+
|  usuarios   |         |  solicitudes   |         | medicamentos |
+-------------+         +----------------+         +--------------+
| id (PK)     |-----\   | id (PK)        |   /-----| id (PK)      |
| email       |     \  | usuario_id(FK) |--/      | nombre       |
| password_hash|     +--| medicamento_id |---------| codigo       |
| nombre      |     /  | es_no_pos      |         | es_pos       |
| creado_en   |    /   | numero_orden   |         | creado_en    |
+-------------+   /    | direccion      |         +--------------+
                  |    | telefono      |
                  |    | correo        |
                  |    | creado_en     |
                  |    +----------------+
                  +--- 1:N  (un usuario → muchas solicitudes)
                       N:1  (muchas solicitudes → un medicamento)
```

## Relaciones

- **usuarios → solicitudes:** 1 a N. Un usuario puede tener muchas solicitudes.
- **medicamentos → solicitudes:** 1 a N. Un medicamento puede aparecer en muchas solicitudes.
- **solicitudes:** cuando el medicamento es NO POS (`es_no_pos = true`), en la API son obligatorios numero_orden, direccion, telefono y correo; en la BD esos campos están como nullable y la regla se aplica en el backend.
