# Cloud API (FastAPI + Redis + MinIO)

API en **FastAPI** con autenticación por token (Redis) y gestión de ficheros en **MinIO**.  
Se incluye configuración con **Docker** y **Docker Compose** para levantar los servicios fácilmente.

---

## 🚀 Requisitos

- Docker y Docker Compose
- Puertos libres:
  - **8000** → API
  - **9000/9001** → MinIO

---

## ▶ Ejecución

Construir y levantar los contenedores:

```bash
docker compose up --build

La API estará disponible en:
http://localhost:8000/docs

 Endpoints principales
Auth

POST /auth/register → Registro de usuario

POST /auth/login → Login (devuelve token)

POST /auth/logout → Logout

GET /auth/introspect → Verificar token

Files

GET /files → Listar ficheros

POST /files → Crear fichero (requiere token)

GET /files/{fid} → Obtener fichero

DELETE /files/{fid} → Eliminar fichero

POST /files/{fid} → Subir contenido

🐳 Imagen en Docker Hub

La imagen se encuentra disponible en:
marudevv/cloud-api

Para descargarla y ejecutar:
docker pull marudevv/cloud-api:latest
docker run -p 8000:8000 marudevv/cloud-api:latest

Ejemplo de uso con curl
Registro
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "marc", "password": "1234"}'

Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "marc", "password": "1234"}'


(guarda el token de la respuesta)

Subir un fichero
curl -X POST "http://localhost:8000/files" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/ruta/a/mi_fichero.txt"

Listar ficheros
curl -X GET "http://localhost:8000/files" \
  -H "Authorization: Bearer <TOKEN>"


Autor: Marc García Izquierdo
```
