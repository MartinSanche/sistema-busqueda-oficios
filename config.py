# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base de la aplicación."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-por-defecto-solo-desarrollo')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    APP_NAME = os.getenv('APP_NAME', 'Sistema de Búsqueda de Oficios')

    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///oficios.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evita warnings innecesarios