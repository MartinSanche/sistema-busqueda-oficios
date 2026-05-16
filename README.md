# 🔧 Sistema de Búsqueda de Oficios

Aplicación web para conectar personas con profesionales de oficios en su área.

## 👥 Equipo
- Estudiante 1 - Tech Lead
- Estudiante 2 - Backend Dev
- Estudiante 3 - Frontend Dev
- Estudiante 4 - DB Dev
- Estudiante 5 - QA / Docs

## 🛠️ Tecnologías
- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite → PostgreSQL
- HTML, CSS, JavaScript

## 🚀 Cómo ejecutar el proyecto

Abrir la terminal Git Bash dentro de la carpeta donde vamos a copiar el repositorio y seguir los siguientes comandos.

### 1. Clonar el repositorio
- git clone https://github.com/MartinSanche/sistema-busqueda-oficios.git

### 2. Crear y activar entorno virtual
- cd sistema-busqueda-oficios
- python -m venv venv
- source venv/Scripts/activate  # Git Bash Windows
- source venv/bin/activate      # Mac/Linux

### 3. Instalar dependencias
- pip install -r requirements.txt

### 4. Configurar variables de entorno
- cp .env.example .env

### 5. Inicializar la base de datos
- flask db upgrade
- python poblar_db.py

### 6. Ejecutar la aplicación
- python run.py

## 🔗 Rutas disponibles

### Páginas
| Ruta | Descripción |
|------|-------------|
| `/` | Página principal |
| `/buscar` | Buscar profesionales |
| `/profesional/<id>` | Perfil del profesional |
| `/contactar/<id>` | Contactar profesional |
| `/registro` | Registro de usuarios |

### API
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/api/status` | GET | Estado de la API |
| `/api/oficios` | GET | Lista todos los oficios |
| `/api/profesionales` | GET | Lista profesionales |
| `/api/profesionales/filtrar` | GET | Filtrar por oficio/ubicacion/experiencia |
| `/api/buscar` | GET | Busca por oficio/ubicación |
| `/api/profesional/<id>` | GET | Detalle de profesional |
| `/api/profesional/<id>/valorar` | POST | Valorar profesional |
| `/api/registro` | POST | Registrar usuario |
| `/api/contacto` | POST | Contactar profesional |

## 📅 Estado del proyecto
- [x] Etapa 1: Configuración del entorno
- [x] Etapa 2: Backend básico con Flask
- [x] Etapa 3: Base de datos con SQLAlchemy
- [x] Etapa 4: Frontend básico
- [x] Etapa 5: Integración frontend-backend
- [x] Etapa 6: Funcionalidades principales
- [ ] Etapa 7: Autenticación
- [ ] Etapa 8: Mejora de UI/UX
- [ ] Etapa 9: Deploy

## 📁 Estructura del proyecto
sistema-busqueda-oficios/
├── app/
│   ├── templates/       ← Archivos HTML
│   ├── static/          ← CSS, JS, imágenes
│   ├── __init__.py      ← Inicializa Flask y DB
│   ├── models.py        ← Modelos de base de datos
│   └── routes.py        ← Rutas y API
├── migrations/          ← Migraciones de la DB
├── docs/                ← Documentación
├── tests/               ← Pruebas
├── config.py            ← Configuración
├── run.py               ← Punto de entrada
├── poblar_db.py         ← Script de datos de prueba
└── requirements.txt     ← Dependencias


## Resumen del proyecto: Sistema de Búsqueda de Oficios

Es una aplicación web desarrollada con **Python + Flask** que conecta personas con profesionales de oficios (plomeros, electricistas, carpinteros, etc.) en su zona.

---

### ¿Qué hace la app?

Funciona como un **directorio de profesionales** donde los usuarios pueden:

- **Buscar** profesionales filtrando por oficio, ubicación y años de experiencia
- **Ver el perfil** de cada profesional con sus datos de contacto y valoraciones
- **Contactar** directamente al profesional mediante un formulario
- **Registrarse** como usuario o como profesional
- **Valorar** a los profesionales con una puntuación del 1 al 5

---

### Stack tecnológico

- **Backend:** Python 3.11 + Flask, con arquitectura de Blueprint
- **Base de datos:** SQLite (con posibilidad de migrar a PostgreSQL), gestionada con SQLAlchemy y Flask-Migrate
- **Frontend:** HTML, CSS y JavaScript vanilla consumiendo una API REST propia
- **Seguridad:** Hashing de contraseñas con Werkzeug, preparación para autenticación con Flask-Login

---

### Arquitectura del proyecto

El proyecto sigue el patrón **MVC adaptado a Flask**. Los modelos principales son cuatro: `Oficio`, `Usuario`, `Profesional` y `Valoracion`, con relaciones entre ellos. Las rutas están divididas en páginas HTML y endpoints de API REST bajo `/api/`.

---

### Estado actual

Las funcionalidades core están completas. Quedan pendientes autenticación completa, mejoras de UI/UX y el deploy a producción.
