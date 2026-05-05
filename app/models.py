# app/models.py
from datetime import datetime
from app import db


class Oficio(db.Model):
    """Tabla de oficios disponibles (plomero, electricista, etc)."""

    __tablename__ = 'oficios'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    icono       = db.Column(db.String(50), default='🔧')
    activo      = db.Column(db.Boolean, default=True)

    # Relación: un oficio tiene muchos profesionales
    profesionales = db.relationship('Profesional', backref='oficio', lazy=True)

    def to_dict(self):
        """Convierte el objeto a diccionario (para respuestas JSON)."""
        return {
            'id':           self.id,
            'nombre':       self.nombre,
            'descripcion':  self.descripcion,
            'icono':        self.icono,
            'activo':       self.activo
        }

    def __repr__(self):
        return f'<Oficio {self.nombre}>'


class Usuario(db.Model):
    """Tabla de usuarios registrados."""

    __tablename__ = 'usuarios'

    id               = db.Column(db.Integer, primary_key=True)
    nombre           = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(120), unique=True, nullable=False)
    password_hash    = db.Column(db.String(255), nullable=False)
    es_profesional   = db.Column(db.Boolean, default=False)
    fecha_registro   = db.Column(db.DateTime, default=datetime.utcnow)
    activo           = db.Column(db.Boolean, default=True)

    # Relación: un usuario puede tener un perfil profesional
    perfil = db.relationship('Profesional', backref='usuario', uselist=False)

    def to_dict(self):
        return {
            'id':             self.id,
            'nombre':         self.nombre,
            'email':          self.email,
            'es_profesional': self.es_profesional,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Profesional(db.Model):
    """Tabla de perfiles profesionales."""

    __tablename__ = 'profesionales'

    id               = db.Column(db.Integer, primary_key=True)
    usuario_id       = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    oficio_id        = db.Column(db.Integer, db.ForeignKey('oficios.id'), nullable=False)
    descripcion      = db.Column(db.String(500))
    ubicacion        = db.Column(db.String(150), nullable=False)
    telefono         = db.Column(db.String(20))
    experiencia_anios = db.Column(db.Integer, default=0)
    disponible       = db.Column(db.Boolean, default=True)

    valoraciones = db.relationship('Valoracion', backref='profesional', lazy=True)

    def promedio_valoraciones(self):
        if not self.valoraciones:
            return 0
        return round(sum(v.puntuacion for v in self.valoraciones) / len(self.valoraciones), 1)

    def to_dict(self):
        return {
            'id':                 self.id,
            'nombre':             self.usuario.nombre,
            'oficio':             self.oficio.nombre,
            'descripcion':        self.descripcion,
            'ubicacion':          self.ubicacion,
            'telefono':           self.telefono,
            'experiencia_anios':  self.experiencia_anios,
            'disponible':         self.disponible,
            'valoracion':         self.promedio_valoraciones(),
            'total_valoraciones': len(self.valoraciones)
        }

    def __repr__(self):
        return f'<Profesional {self.usuario_id}>'
    
    
    
    
    
class Valoracion(db.Model):
    """Tabla de valoraciones de profesionales."""

    __tablename__ = 'valoraciones'

    id             = db.Column(db.Integer, primary_key=True)
    profesional_id = db.Column(db.Integer, db.ForeignKey('profesionales.id'), nullable=False)
    puntuacion     = db.Column(db.Integer, nullable=False)  # 1 a 5
    comentario     = db.Column(db.String(500))
    fecha          = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':             self.id,
            'profesional_id': self.profesional_id,
            'puntuacion':     self.puntuacion,
            'comentario':     self.comentario,
            'fecha':          self.fecha.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f'<Valoracion {self.puntuacion}>'