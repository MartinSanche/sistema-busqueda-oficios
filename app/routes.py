# app/routes.py
from flask import redirect
from flask_login import login_user, logout_user, login_required, current_user
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

    if not data or not all(k in data for k in ['nombre', 'email', 'password']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 409

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        es_profesional=data.get('es_profesional', False)
    )
    nuevo_usuario.set_password(data['password'])

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


{% extends 'base.html' %}

{% block title %}Buscar — Búsqueda de Oficios{% endblock %}

{% block content %}
<section class="section">
    <h2>🔍 Buscar profesionales</h2>

    <!-- FORMULARIO DE BÚSQUEDA -->
    <div class="search-box">
        <div class="search-fields">
            <div class="field">
                <label for="oficio">Oficio</label>
                <input type="text" id="oficio"
                    placeholder="Ej: Plomero, Electricista...">
            </div>
            <div class="field">
                <label for="ubicacion">Ubicación</label>
                <input type="text" id="ubicacion"
                    placeholder="Ej: Buenos Aires, Córdoba...">
            </div>
            <div class="field" style="max-width: 180px">
                <label for="experiencia">Experiencia mínima</label>
                <select id="experiencia" style="width:100%; padding: 10px 14px;
                    border: 1px solid #ddd; border-radius: 8px; font-size: 1rem;
                    background: white; color: #333">
                    <option value="0">Cualquiera</option>
                    <option value="1">1+ años</option>
                    <option value="3">3+ años</option>
                    <option value="5">5+ años</option>
                    <option value="10">10+ años</option>
                </select>
            </div>
            <button class="btn btn-primary" onclick="buscar()">
                🔍 Buscar
            </button>
        </div>
    </div>

    <!-- RESULTADOS -->
    <div id="resultados">
        <p class="hint">Ingresá un oficio o ubicación para buscar profesionales</p>
    </div>
</section>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script>
    window.onload = function() {
        const params = new URLSearchParams(window.location.search)
        const oficio = params.get('oficio')
        if (oficio) {
            document.getElementById('oficio').value = oficio
            buscar()
        }
    }

    async function buscar() {
        const oficio      = document.getElementById('oficio').value.trim()
        const ubicacion   = document.getElementById('ubicacion').value.trim()
        const experiencia = document.getElementById('experiencia').value

        if (!oficio && !ubicacion) {
            mostrarVacio('resultados', 'Ingresá al menos un criterio de búsqueda')
            return
        }

        mostrarLoading('resultados', 'Buscando profesionales...')

        try {
            const params = new URLSearchParams()
            if (oficio)      params.append('oficio', oficio)
            if (ubicacion)   params.append('ubicacion', ubicacion)
            if (experiencia) params.append('experiencia', experiencia)

            const response = await fetch(`/api/profesionales/filtrar?${params}`)
            const data = await response.json()
            mostrarResultados(data)
        } catch (error) {
            mostrarError('resultados', 'Error al buscar. Intentá de nuevo.')
        }
    }

    function mostrarResultados(data) {
        const div = document.getElementById('resultados')

        if (data.total === 0) {
            mostrarVacio('resultados', '😕 No se encontraron profesionales')
            return
        }

        div.innerHTML = `
            <p class="total">
                Se encontraron <strong>${data.total}</strong> profesionales
            </p>
        `
        data.resultados.forEach(p => {
            div.innerHTML += `
                <div class="card-profesional">
                    <div class="prof-header">
                        <h3>${p.nombre}</h3>
                        <span class="badge">${p.oficio}</span>
                    </div>
                    <p>${p.descripcion || 'Sin descripción'}</p>
                    <div class="prof-info">
                        <span>📍 ${p.ubicacion}</span>
                        <span>⏱ ${p.experiencia_anios} años de experiencia</span>
                        <span>📞 ${p.telefono || 'Sin teléfono'}</span>
                    </div>
                    <div style="margin-top: 12px; display: flex; gap: 8px">
                        <a href="/profesional/${p.id}" class="btn btn-secondary">
                            Ver perfil
                        </a>
                        <a href="/contactar/${p.id}" class="btn btn-primary"
                           style="font-size: 0.9rem; padding: 8px 18px">
                            📬 Contactar
                        </a>
                    </div>
                </div>
            `
        })
    }

    document.addEventListener('DOMContentLoaded', () => {
        ['oficio', 'ubicacion'].forEach(id => {
            document.getElementById(id).addEventListener('keypress', e => {
                if (e.key === 'Enter') buscar()
            })
        })
    })
</script>
{% endblock %}

@main.route('/contactar/<int:id>')
def contactar_page(id):
    """Página de formulario de contacto."""
    return render_template('contactar.html', profesional_id=id)

@main.route('/api/profesionales/filtrar')
def filtrar_profesionales():
    """Filtra profesionales por múltiples criterios."""
    oficio      = request.args.get('oficio', '')
    ubicacion   = request.args.get('ubicacion', '')
    experiencia = request.args.get('experiencia', 0, type=int)
    disponible  = request.args.get('disponible', 'true') == 'true'

    query = Profesional.query.filter_by(disponible=disponible)

    if oficio:
        query = query.join(Oficio).filter(
            Oficio.nombre.ilike(f'%{oficio}%')
        )
    if ubicacion:
        query = query.filter(
            Profesional.ubicacion.ilike(f'%{ubicacion}%')
        )
    if experiencia:
        query = query.filter(
            Profesional.experiencia_anios >= experiencia
        )

    resultados = query.all()
    return jsonify({
        'resultados': [p.to_dict() for p in resultados],
        'total':      len(resultados)
    })


@main.route('/api/profesional/<int:id>/valorar', methods=['POST'])
def valorar_profesional(id):
    """Agrega una valoración a un profesional."""
    from app.models import Valoracion
    data = request.get_json()

    if not data or 'puntuacion' not in data:
        return jsonify({'error': 'Puntuación requerida'}), 400

    puntuacion = data.get('puntuacion')
    if not 1 <= puntuacion <= 5:
        return jsonify({'error': 'Puntuación debe ser entre 1 y 5'}), 400

    valoracion = Valoracion(
        profesional_id=id,
        puntuacion=puntuacion,
        comentario=data.get('comentario', '')
    )
    db.session.add(valoracion)
    db.session.commit()

    return jsonify({'mensaje': 'Valoración guardada correctamente'}), 201

@main.route('/login')
def login_page():
    """Página de login."""
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('login.html')


@main.route('/api/login', methods=['POST'])
def login():
    """Inicia sesión."""
    from flask import redirect
    data = request.get_json()

    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Email y contraseña requeridos'}), 400

    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not usuario.check_password(data['password']):
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401

    if not usuario.activo:
        return jsonify({'error': 'Cuenta desactivada'}), 401

    login_user(usuario, remember=data.get('remember', False))

    return jsonify({
        'mensaje': f'Bienvenido/a, {usuario.nombre}!',
        'usuario': usuario.to_dict()
    })


@main.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Cierra sesión."""
    logout_user()
    return jsonify({'mensaje': 'Sesión cerrada correctamente'})


@main.route('/api/me')
def me():
    """Devuelve el usuario logueado o null."""
    if current_user.is_authenticated:
        return jsonify({'usuario': current_user.to_dict()})
    return jsonify({'usuario': None})


@main.route('/mi-perfil')
@login_required
def mi_perfil():
    """Página del perfil del usuario logueado."""
    return render_template('mi_perfil.html')

