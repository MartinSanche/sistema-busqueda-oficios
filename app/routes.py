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

@main.route('/buscar')
def buscar_page():
    """Página de búsqueda."""
    return render_template('buscar.html')


from werkzeug.security import generate_password_hash

@main.route('/api/registro', methods=['POST'])
def registro():
    """Registra un nuevo usuario."""
    data = request.get_json()

    # Validaciones básicas
    if not data or not all(k in data for k in ['nombre', 'email', 'password']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verificar que el email no exista
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 409

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        es_profesional=data.get('es_profesional', False)
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        'mensaje': 'Usuario registrado exitosamente',
        'usuario': nuevo_usuario.to_dict()
    }), 201


@main.route('/api/contacto', methods=['POST'])
def contactar_profesional():
    """Registra una solicitud de contacto hacia un profesional."""
    data = request.get_json()

    if not data or not all(k in data for k in ['profesional_id', 'nombre_contacto', 'mensaje']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    profesional = Profesional.query.get(data['profesional_id'])
    if not profesional:
        return jsonify({'error': 'Profesional no encontrado'}), 404

    # Por ahora devolvemos éxito (en etapas futuras se puede enviar email)
    return jsonify({
        'mensaje': f'Solicitud enviada a {profesional.usuario.nombre}',
        'profesional': profesional.to_dict()
    }), 200

@main.route('/registro')
def registro_page():
    return render_template('registro.html')    

@main.route('/api/profesional/<int:id>')
def obtener_profesional(id):
    """Obtiene el detalle de un profesional por ID."""
    profesional = Profesional.query.get_or_404(id)
    return jsonify(profesional.to_dict())


@main.route('/profesional/<int:id>')
def detalle_profesional(id):
    """Página de detalle de un profesional."""
    return render_template('detalle.html', profesional_id=id)

