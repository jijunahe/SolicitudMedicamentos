# Solicitud de Medicamentos

App full stack para gestionar solicitudes de medicamentos (POS y NO POS). Backend en FastAPI, front en React, MySQL de base. Sale de una prueba técnica; está armada en capas, con auth aparte y JWT.

---

## Qué hay en el repo

- **backend/** — API en Python (FastAPI). Modelos, servicios, controladores, JWT, MySQL.
- **frontend/** — React con Vite. Habla con la API (los consumos van al backend).
- **documentacion/** — Enunciado de la prueba.
- **docs/** — Arquitectura y modelo entidad-relación.
- **docker-compose.yml** — Para levantar MySQL + backend + front si querés usar Docker.

---

## Requisitos

Para correr en local: Python 3.10+, Node 20+, MySQL 8.  
O solo Docker y listo.

---

## Cómo correrlo

### Con Docker (todo en uno)

Con un solo comando tenés MySQL, backend y frontend. Las tablas y las semillas (medicamentos + usuario nevaEps) las crea el backend al arrancar; no hace falta ejecutar ningún SQL.

```bash
cp .env.example .env
docker compose up -d --build
```

Entrás a:
- **Front:** http://localhost:3000
- **API (Swagger):** http://localhost:8000/docs
- **MySQL:** localhost:3308 (usuario `eps`, pass `12345678`) — puerto 3308 para no chocar con MySQL/MariaDB en el host

Si en algún momento la base quedó rara o querés empezar de cero, bajá los contenedores y el volumen y volvé a subir:

```bash
docker compose down -v
docker compose up -d --build
```

### Sin Docker (local)

**1. MySQL**

Creá la base y el usuario. Como root de MySQL:

```bash
sudo mysql < backend/scripts/init_db.sql
```

(o `mysql -u root -p < backend/scripts/init_db.sql` si tu root tiene clave).

Si solo creaste la base vacía, no pasa nada: al arrancar el backend se crean las tablas y se cargan las semillas solas (medicamentos de ejemplo + usuario `nevaEps@eps.local` / `12345678`).

En la raíz del repo (o en `backend/`) tené un `.env` (podés copiar de `.env.example`) con algo así:

```env
DB_USER=eps
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=3306
DB_NAME=solicitud_medicamentos
JWT_SECRET_KEY=algo-secreto-cambialo-en-produccion

# Usuario inicial que se crea en la semilla al arrancar (opcional)
SEED_USER_EMAIL=nevaEps@eps.local
SEED_USER_PASSWORD=12345678
SEED_USER_NOMBRE=nevaEps
```

**2. Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**3. Frontend**

```bash
cd frontend
npm install
npm run dev
```

(O `npm run build` y `npm run preview` si `npm run dev` te da el error de “too many open files”.)

El front corre en http://localhost:3000 y el proxy apunta las llamadas `/api` al backend. La URL del backend en dev se configura con `VITE_PROXY_TARGET` en el `.env` del frontend (por defecto `http://localhost:8000`). Copiá `frontend/.env.example` a `frontend/.env` si querés cambiarla.

---

## Documentación de la API (Swagger)

La API está documentada con **Swagger UI**. Con el backend levantado:

- **Swagger (interfaz para probar):** http://localhost:8000/docs  
- **ReDoc (solo lectura):** http://localhost:8000/redoc  

Ahí ves todos los endpoints, los esquemas de request/response y podés probar las llamadas desde el navegador (login, register, crear solicitud, etc.). Para los endpoints que piden auth, hacé primero POST `/auth/login`, copiá el `access_token` y en Swagger usá el botón “Authorize” y pegá: `Bearer <tu_token>`.

**Endpoints:**

| Método | Ruta | Qué hace |
|--------|------|----------|
| POST | `/auth/register` | Registrar usuario (la pass se guarda hasheada) |
| POST | `/auth/login` | Login; devuelve el JWT |
| GET | `/medicamentos` | Lista de medicamentos (público) |
| POST | `/solicitudes` | Crear solicitud (requiere token) |
| GET | `/solicitudes` | Listar tus solicitudes, paginado (requiere token) |

Los que piden token: en la cabecera `Authorization: Bearer <token>`.

**Solicitudes NO POS:** si el medicamento es NO POS, en el body tenés que mandar sí o sí `numero_orden`, `direccion`, `telefono` y `correo`. Si es POS, esos campos no van.

---

## Base de datos y semillas

Al arrancar el backend se crean las tablas (si no existen) y se ejecutan las semillas: 5 medicamentos de ejemplo y un usuario inicial. El usuario inicial sale de las variables de entorno `SEED_USER_EMAIL`, `SEED_USER_PASSWORD` y `SEED_USER_NOMBRE` (por defecto: nevaEps@eps.local / 12345678). Si dejás `SEED_USER_EMAIL` vacío, no se crea ningún usuario de semilla. Es idempotente: si ya hay datos, no los vuelve a insertar.

Tablas: `usuarios`, `medicamentos`, `solicitudes`. Modelo ER en `docs/MODELO_ER.md`.  
Scripts SQL por si querés hacer todo a mano: `backend/scripts/init_db.sql`, `backend/scripts/crear_tablas.sql`, `backend/scripts/borrar_tablas.sql` (este último para vaciar y probar de nuevo las semillas).

---

## Variables de entorno (.env)

| Variable | Descripción |
|----------|-------------|
| `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` | Conexión MySQL |
| `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | JWT |
| `SEED_USER_EMAIL`, `SEED_USER_PASSWORD`, `SEED_USER_NOMBRE` | Usuario inicial que se crea en la semilla al arrancar. Si `SEED_USER_EMAIL` está vacío, no se crea usuario. |

**Frontend** (en `frontend/.env`, opcional): `VITE_PROXY_TARGET` — URL del backend para el proxy en desarrollo (por defecto `http://localhost:8000`). `VITE_API_URL` — base URL de la API en el cliente (por defecto `/api`).

Copiá `.env.example` a `.env` (y `frontend/.env.example` a `frontend/.env` si usás el front en local) y ajustá los valores.

## Seguridad

Passwords con bcrypt. Sesión con JWT. Todo lo sensible (DB, JWT, usuario semilla) va por `.env`.

---

## Stack

Backend: Python, FastAPI, Uvicorn, SQLAlchemy, PyMySQL, PyJWT, pydantic-settings.  
Front: React 18, Vite, React Router, Axios.  
BD: MySQL 8.
