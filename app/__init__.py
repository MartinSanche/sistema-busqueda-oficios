# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Crear instancias globales
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Crea y configura la aplicación Flask."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rutas
    from app.routes import main
    app.register_blueprint(main)

    return app