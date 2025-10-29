# Task Management API

Una API REST simple para la gestión de tareas construida con **FastAPI** siguiendo principios de **Arquitectura Hexagonal** y **SOLID**.

## Descripción del Proyecto

Esta es una aplicación de ejemplo que demuestra una arquitectura limpia y escalable para una API REST. La aplicación permite crear, leer, actualizar y eliminar tareas con validaciones robustas.

### Características Principales

- ✅ CRUD completo de tareas
- 📊 Arquitectura Hexagonal (Puertos y Adaptadores)
- 🏗️ Separación clara de responsabilidades (SOLID)
- 🐳 Containerización con Docker
- 📚 Documentación automática con Swagger UI
- ⚡ Framework moderno con FastAPI
- 🔍 Validación robusta de datos con Pydantic

## Requisitos Previos

Para ejecutar este proyecto necesitas:

- **Docker** (versión 20.10 o superior) - [Instalar Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (opcional, para orchestración)
- **Python 3.11+** (si ejecutas sin Docker)
- **pip** (para gestionar dependencias)

## Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

#### 1. Build de la imagen Docker

```bash
docker build -t task-api:latest .
```

**Desglose del comando:**
- `docker build`: Construye una nueva imagen Docker
- `-t task-api:latest`: Etiqueta la imagen con nombre `task-api` y versión `latest`
- `.`: Usa el Dockerfile en el directorio actual

#### 2. Ejecutar el contenedor

```bash
docker run -p 8000:8000 task-api:latest
```

**Desglose del comando:**
- `docker run`: Crea y ejecuta un contenedor
- `-p 8000:8000`: Mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina
- `task-api:latest`: Usa la imagen que construimos

**Salida esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Opción 2: Sin Docker (Desarrollo Local)

#### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd <directorio-del-proyecto>
```

#### 2. Crear un entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Ejecutar la aplicación

```bash
python -m uvicorn app.adapters.http.fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

**Opciones disponibles:**
- `--reload`: Reinicia el servidor cuando detecta cambios en el código (desarrollo)
- `--host 0.0.0.0`: Escucha en todas las interfaces de red
- `--port 8000`: Puerto de escucha

## Uso de la API

### Acceso a la documentación

Una vez que la aplicación esté en ejecución, accede a:

- **Swagger UI** (interfaz interactiva): http://localhost:8000/docs
- **ReDoc** (documentación alternativa): http://localhost:8000/redoc

### Endpoints Disponibles

#### 1. Health Check
Verifica que la API está en funcionamiento.

```bash
curl -X GET http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "ok"
}
```

---

#### 2. Listar todas las tareas

```bash
curl -X GET http://localhost:8000/tasks
```

**Respuesta:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Estudiar arquitectura de software",
    "status": "pending"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Hacer el parcial",
    "status": "done"
  }
]
```

---

#### 3. Crear una nueva tarea

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudiar arquitectura de software",
    "status": "pending"
  }'
```

**Request Body:**
```json
{
  "title": "Estudiar arquitectura de software",
  "status": "pending"
}
```

**Respuesta (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Estudiar arquitectura de software",
  "status": "pending"
}
```

**Validaciones:**
- `title`: Requerido, no puede estar vacío
- `status`: Opcional, por defecto es `"pending"`, acepta `"pending"` o `"done"`

---

#### 4. Obtener una tarea por ID

```bash
curl -X GET http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Respuesta:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Estudiar arquitectura de software",
  "status": "pending"
}
```

**Errores:**
- `404 Not Found`: Si la tarea no existe

---

#### 5. Actualizar una tarea

```bash
curl -X PUT http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudiar arquitectura de software - Parcial",
    "status": "done"
  }'
```

**Request Body:**
```json
{
  "title": "Estudiar arquitectura de software - Parcial",
  "status": "done"
}
```

**Respuesta:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Estudiar arquitectura de software - Parcial",
  "status": "done"
}
```

**Nota:** Tanto `title` como `status` son opcionales. Solo se actualizan los campos proporcionados.

---

#### 6. Eliminar una tarea

```bash
curl -X DELETE http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Respuesta:** `204 No Content` (sin body)

**Errores:**
- `404 Not Found`: Si la tarea no existe

---

## Arquitectura

### Estructura del Proyecto

```
app/
├── domain/                          # Capa de Dominio
│   └── task.py                      # Modelo de dominio: Task
│
├── application/                     # Capa de Aplicación
│   ├── ports/                       # Puertos (Interfaces/Contratos)
│   │   └── task_repository.py       # Interfaz del repositorio
│   │
│   └── services/                    # Servicios de Aplicación
│       └── task_service.py          # Lógica de negocio
│
└── adapters/                        # Capa de Adaptadores
    ├── http/                        # Adaptador HTTP
    │   └── fastapi_app.py           # Aplicación FastAPI
    │
    └── persistence/                 # Adaptador de Persistencia
        └── memory_task_repository.py # Repositorio en memoria
```

### Patrones Utilizados

#### Arquitectura Hexagonal (Puertos y Adaptadores)

La aplicación está dividida en capas bien definidas:

1. **Domain**: Contiene la lógica de negocio pura (entities y value objects)
2. **Application**: Contiene los casos de uso y servicios
3. **Adapters**: Contiene las implementaciones específicas de tecnología

#### Principios SOLID

- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Abierto para extensión, cerrado para modificación
- **L**iskov Substitution: Los adaptadores pueden reemplazarse sin afectar la lógica
- **I**nterface Segregation: Las interfaces son específicas y pequeñas
- **D**ependency Inversion: Dependemos de abstracciones, no de implementaciones

## Modelos de Datos

### Task (Entidad de Dominio)

```python
@dataclass
class Task:
    id: str                             # UUID único generado automáticamente
    title: str                          # Título de la tarea (requerido)
    status: Literal["pending", "done"]  # Estado: "pending" o "done"

    # Métodos de negocio
    def mark_done(self) -> None:        # Marca la tarea como completada
    def mark_pending(self) -> None:     # Marca la tarea como pendiente
```

### Esquemas HTTP

#### TaskCreateRequest
```python
{
    "title": str,           # Requerido, mínimo 1 carácter
    "status": str = "pending"  # Opcional
}
```

#### TaskUpdateRequest
```python
{
    "title": str = None,    # Opcional
    "status": str = None    # Opcional
}
```

#### TaskResponse
```python
{
    "id": str,
    "title": str,
    "status": str
}
```

## Dependencias

Todas las dependencias están especificadas en `requirements.txt`:

- **fastapi** ≥ 0.109.0 - Framework web moderno
- **uvicorn** ≥ 0.25.0 - Servidor ASGI
- **pydantic** ≥ 2.7.0 - Validación de datos

Para ver las versiones exactas:

```bash
cat requirements.txt
```

## Comandos Útiles

### Docker

```bash
# Construir la imagen
docker build -t task-api:latest .

# Ejecutar el contenedor
docker run -p 8000:8000 task-api:latest

# Ver contenedores en ejecución
docker ps

# Detener un contenedor
docker stop <container_id>

# Ver logs de un contenedor
docker logs <container_id>

# Eliminar la imagen
docker rmi task-api:latest
```

### Desarrollo Local

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con hot-reload
python -m uvicorn app.adapters.http.fastapi_app:app --host 0.0.0.0 --port 8000 --reload

# Desactivar entorno virtual
deactivate
```

## Solución de Problemas

### Puerto 8000 ya está en uso

Si ves el error `Address already in use`:

```bash
# Cambiar el puerto
docker run -p 8001:8000 task-api:latest

# O matar el proceso que usa el puerto
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Problemas al construir la imagen Docker

Asegúrate de tener Docker corriendo y estar en el directorio correcto:

```bash
# Verificar que Docker está corriendo
docker --version

# Estar en el directorio del proyecto
cd "c:\Users\Esteban Molina\OneDrive - Universidad EAFIT\Escritorio\EAFIT\SEMESTRE 6\Arquitectura De Software\Parcial 2 Examen Practico"

# Verificar que Dockerfile existe
ls Dockerfile
```

### La API no responde

1. Verifica que el contenedor está en ejecución: `docker ps`
2. Verifica los logs: `docker logs <container_id>`
3. Intenta acceder a http://localhost:8000/health

## Notas Importantes

- **Almacenamiento**: La aplicación usa un repositorio en memoria. Los datos se pierden cuando se reinicia.
- **Estado Inicial**: La aplicación comienza sin tareas. Debes crearlas mediante la API.
- **Validación**: Todas las entradas son validadas por Pydantic antes de procesarse.

## Próximas Mejoras

- [ ] Persistencia en base de datos (PostgreSQL, MongoDB)
- [ ] Autenticación y autorización
- [ ] Paginación de resultados
- [ ] Filtros avanzados
- [ ] Pruebas unitarias e integración
- [ ] Logging centralizado
- [ ] Rate limiting

## Licencia

Este proyecto es de propósito educativo.

## Contacto

Para preguntas o sugerencias sobre este proyecto, contacta a tu instructor.

---

**Última actualización:** Octubre 2025
