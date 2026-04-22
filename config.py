# config.py
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class Config:
    """Configuración base de la aplicación."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-por-defecto-solo-desarrollo')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///oficios.db')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    
    # Nombre de la app
    APP_NAME = os.getenv('APP_NAME', 'Sistema de Búsqueda de Oficios')