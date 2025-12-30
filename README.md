# Task Management API

API REST para gestión de tareas construida con FastAPI, SQLAlchemy y PostgreSQL.

## Tecnologías

- **Python 3.11.8**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **JWT** - Autenticación con tokens
- **Bcrypt** - Hash seguro de contraseñas
- **Alembic** - Migraciones de base de datos
- **Docker** - Contenedorización de PostgreSQL

##  Funcionalidades

- Autenticación JWT con usuario inicial automático
- CRUD completo de tareas
- Paginación en listado de tareas
- Hash seguro de contraseñas con bcrypt
- Migraciones automáticas con Alembic
- Manejo de errores HTTP (400/401/404/422)
- Arquitectura modular con servicios

## Arquitectura

```
app/
├── api/          # Endpoints y routers
├── core/         # Configuración, seguridad, JWT
├── db/           # Sesión, conexión, migraciones
├── models/       # Modelos SQLAlchemy
├── schemas/      # Esquemas Pydantic
├── services/     # Lógica de negocio
└── main.py       # Punto de entrada
```

## Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=api_test
DB_USER=postgres
DB_PASSWORD=postgres
JWT_SECRET=clave_secreta_aqui
JWT_EXPIRE_MINUTES=30
```

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd fastapi-test
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Levantar PostgreSQL con Docker
```bash
docker-compose up -d
```

### 5. Ejecutar migraciones
```bash
alembic upgrade head
```

### 6. Iniciar la aplicación
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`
Documentación interactiva: `http://localhost:8000/docs`

## Usuario Inicial

El sistema crea automáticamente un usuario inicial mediante migraciones:

- **Email**: `admin@test.com`
- **Password**: `admin123`

**Creación automática**: El usuario se crea automáticamente al ejecutar `alembic upgrade head` mediante la migración `5a025f5b928c_add_initial_user.py`.

## Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/register` - Registrar usuario
- `GET /auth/me` - Obtener usuario actual

### Tareas
- `POST /tasks/` - Crear tarea
- `GET /tasks/` - Listar tareas (con paginación)
- `GET /tasks/{id}` - Obtener tarea específica
- `PUT /tasks/{id}` - Actualizar tarea
- `DELETE /tasks/{id}` - Eliminar tarea

## Ejemplos de Uso

### 1. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Crear Tarea
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Descripción de la tarea",
    "status": "pending"
  }'
```

### 3. Listar Tareas (con paginación)
```bash
curl -X GET "http://localhost:8000/tasks/?page=1&page_size=10" \
  -H "Authorization: Bearer <tu_token>"
```

### 4. Actualizar Tarea
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "done"
  }'
```

## Modelo de Datos

### Task
- `id` (Integer, PK) - Identificador único
- `title` (String, required) - Título de la tarea
- `description` (String, optional) - Descripción detallada
- `status` (Enum) - Estado: pending/in_progress/done
- `created_at` (DateTime) - Fecha de creación
- `owner_id` (Integer, FK) - ID del usuario propietario

### User
- `id` (Integer, PK) - Identificador único
- `email` (String, unique) - Email del usuario
- `hashed_password` (String) - Contraseña hasheada
- `created_at` (DateTime) - Fecha de registro

## Índices de Base de Datos

Se definieron los siguientes índices para optimizar el rendimiento:

1. **`ix_tasks_title`** - Índice en `title` para búsquedas rápidas por título
2. **`ix_tasks_status`** - Índice en `status` para filtros por estado
3. **`ix_tasks_owner_id`** - Índice en `owner_id` para consultas por usuario
4. **`ix_tasks_status_created`** - Índice compuesto en `(status, created_at)` para ordenamiento eficiente
5. **`ix_users_email`** - Índice único en `email` para login rápido

**Justificación**: Estos índices optimizan las consultas más frecuentes: filtros por usuario, estado de tareas, y ordenamiento por fecha de creación.

## Seguridad

- **JWT**: Tokens con expiración configurable
- **Bcrypt**: Hash seguro de contraseñas con salt automático
- **Endpoints protegidos**: Todas las operaciones de tareas requieren autenticación
- **Validación**: Esquemas Pydantic para validación de entrada

## Manejo de Errores

- **400**: Datos inválidos o credenciales incorrectas
- **401**: Token inválido o expirado
- **404**: Recurso no encontrado
- **422**: Error de validación de datos

## Decisiones Técnicas

### Paginación
**Decisión**: Paginación basada en offset/limit con validaciones.
**Parámetros**: `page` (default: 1), `page_size` (default: 10, max: 100).
**Justificación**: Simple de implementar y entender, adecuado para el alcance del proyecto.

### Autenticación
**Decisión**: JWT con identificación por email.
**Trade-off**: Stateless vs. necesidad de invalidación manual.
**Justificación**: Escalable y estándar de la industria.

## Notas de Desarrollo

- El proyecto está configurado para desarrollo local con PostgreSQL en Docker
- Las migraciones se ejecutan automáticamente y crean el usuario inicial
- La documentación interactiva está disponible en `/docs`
- Los logs de desarrollo muestran información útil para debugging