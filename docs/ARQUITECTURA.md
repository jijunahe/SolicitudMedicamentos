# Arquitectura del proyecto

El backend está organizado en capas (tipo MVC pero para API) y con idea de SOA: auth por un lado, solicitudes por otro. El front es una SPA que solo consume la API.

## Cómo está organizado

**Backend (FastAPI)**  
Separación clara: modelos, schemas (Pydantic), servicios (lógica) y controllers (routers). La config y la BD salen de `.env`. JWT y dependencias de auth viven en `core/`.

**Frontend (React)**  
Vistas en `views/`, componentes en `components/`, y las llamadas a la API en `services/`. El estado de login (token) está en un context.

## Estructura de carpetas

```
SolicitudMedicamentos/
├── backend/
│   ├── app/
│   │   ├── main.py          # Entry point, routers, Swagger
│   │   ├── config.py        # Lee el .env
│   │   ├── database.py       # Conexión MySQL (SQLAlchemy)
│   │   ├── models/          # Entidades ORM (Usuario, Medicamento, Solicitud)
│   │   ├── schemas/         # DTOs y validación (Pydantic)
│   │   ├── services/        # Lógica de negocio
│   │   ├── controllers/     # Routers (auth, medicamentos, solicitudes)
│   │   ├── core/            # JWT, bcrypt, dependencias de auth
│   │   └── seed.py          # Semillas al arranque
│   ├── scripts/             # SQL varios (init, borrar tablas, etc.)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/           # Páginas (Login, Register, SolicitudForm, listado)
│   │   ├── components/      # Layout, etc.
│   │   ├── services/        # api.js — axios y llamadas al backend
│   │   └── context/         # AuthContext (token, login, logout)
│   └── Dockerfile
├── documentacion/
├── docs/                    # Este archivo + modelo ER
├── docker-compose.yml
├── .env.example
└── README.md
```

## Módulos (SOA)

- **Auth:** `/auth/login` y `/auth/register`. La pass se guarda hasheada (bcrypt). El login devuelve un JWT y el front lo usa para el resto de llamadas.
- **Medicamentos:** listado público para el selector del formulario (POS y NO POS).
- **Solicitudes:** crear y listar (paginado). Solo con token. Si el medicamento es NO POS, la API exige numero_orden, direccion, telefono y correo; eso se valida en el servicio.

## Seguridad

Passwords con bcrypt. Sesión con JWT (access token). Secret y tiempo de expiración en `.env`. La conexión a MySQL también va por env (usuario, pass, host, nombre de la BD). El usuario inicial de la semilla se configura con `SEED_USER_EMAIL`, `SEED_USER_PASSWORD` y `SEED_USER_NOMBRE`; si el email está vacío, no se crea usuario de semilla.

## Base de datos

Tres tablas: `usuarios` (id, email, password_hash, nombre, creado_en), `medicamentos` (id, nombre, codigo, es_pos, creado_en), `solicitudes` (id, usuario_id, medicamento_id, es_no_pos, numero_orden, direccion, telefono, correo, creado_en). Detalle del modelo en `MODELO_ER.md`; scripts en `backend/scripts/`.
