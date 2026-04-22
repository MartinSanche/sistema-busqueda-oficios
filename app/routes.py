# app/routes.py
from flask import Blueprint, jsonify, render_template

# Crear el blueprint principal
main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Página principal."""
    return render_template('index.html')


@main.route('/api/status')
def status():
    """Ruta de prueba para verificar que la API funciona."""
    return jsonify({
        'status': 'ok',
        'mensaje': 'API del Sistema de Búsqueda de Oficios funcionando',
        'version': '1.0.0'
    })


@main.route('/api/oficios')
def listar_oficios():
    """Lista de oficios de prueba (datos temporales)."""
    oficios = [
        {'id': 1, 'nombre': 'Plomero',    'descripcion': 'Instalaciones de agua'},
        {'id': 2, 'nombre': 'Electricista','descripcion': 'Instalaciones eléctricas'},
        {'id': 3, 'nombre': 'Carpintero', 'descripcion': 'Trabajos en madera'},
    ]
    return jsonify({'oficios': oficios, 'total': len(oficios)})