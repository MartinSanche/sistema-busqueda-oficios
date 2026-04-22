# app/routes.py
from flask import Blueprint, jsonify, render_template, request
from app import db
from app.models import Oficio, Usuario, Profesional

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
    """Lista todos los oficios desde la base de datos."""
    oficios = Oficio.query.filter_by(activo=True).all()
    return jsonify({
        'oficios': [o.to_dict() for o in oficios],
        'total':   len(oficios)
    })


@main.route('/api/profesionales')
def listar_profesionales():
    """Lista todos los profesionales disponibles."""
    profesionales = Profesional.query.filter_by(disponible=True).all()
    return jsonify({
        'profesionales': [p.to_dict() for p in profesionales],
        'total':         len(profesionales)
    })


@main.route('/api/buscar')
def buscar():
    """Busca profesionales por oficio y/o ubicación."""
    oficio    = request.args.get('oficio', '')
    ubicacion = request.args.get('ubicacion', '')

    query = Profesional.query.filter_by(disponible=True)

    if oficio:
        query = query.join(Oficio).filter(
            Oficio.nombre.ilike(f'%{oficio}%')
        )
    if ubicacion:
        query = query.filter(
            Profesional.ubicacion.ilike(f'%{ubicacion}%')
        )

    resultados = query.all()
    return jsonify({
        'resultados': [p.to_dict() for p in resultados],
        'total':      len(resultados)
    })