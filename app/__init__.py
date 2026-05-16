# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Crear instancias globales
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    """Crea y configura la aplicación Flask."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Ruta a la que redirige si no está logueado
    login_manager.login_view = 'main.login_page'
    login_manager.login_message = 'Necesitás iniciar sesión para acceder'

    # Registrar rutas
    from app.routes import main
    app.register_blueprint(main)

    return app