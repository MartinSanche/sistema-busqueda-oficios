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

### API
| Ruta | Descripción |
|------|-------------|
| `/api/status` | Estado de la API |
| `/api/oficios` | Lista todos los oficios |
| `/api/profesionales` | Lista todos los profesionales |
| `/api/buscar?oficio=X&ubicacion=Y` | Busca profesionales |

## 📅 Estado del proyecto
- [x] Etapa 1: Configuración del entorno
- [x] Etapa 2: Backend básico con Flask
- [x] Etapa 3: Base de datos con SQLAlchemy
- [x] Etapa 4: Frontend básico
- [ ] Etapa 5: Integración frontend-backend
- [ ] Etapa 6: Funcionalidades principales
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
