# app/__init__.py
from flask import Flask
from config import Config

def create_app():
    """
    Función que crea y configura la aplicación Flask.
    Este patrón se llama 'Application Factory'.
    """
    
    # Crear la instancia de Flask
    app = Flask(__name__)
    
    # Cargar la configuración
    app.config.from_object(Config)
    
    # Registrar las rutas
    from app.routes import main
    app.register_blueprint(main)
    
    return app