# poblar_db.py
from app import create_app, db
from app.models import Oficio, Usuario, Profesional

app = create_app()

with app.app_context():
    # Crear todas las tablas
    db.create_all()
    print('✅ Tablas creadas')

    # Crear oficios
    oficios = [
        Oficio(nombre='Plomero',      descripcion='Instalaciones y reparaciones de agua', icono='🔧'),
        Oficio(nombre='Electricista', descripcion='Instalaciones eléctricas',              icono='⚡'),
        Oficio(nombre='Carpintero',   descripcion='Trabajos en madera y muebles',          icono='🔨'),
        Oficio(nombre='Pintor',       descripcion='Pintura de interiores y exteriores',    icono='🎨'),
        Oficio(nombre='Albañil',      descripcion='Construcción y reparaciones',           icono='🧱'),
    ]
    db.session.add_all(oficios)
    db.session.commit()
    print('✅ Oficios creados')

    # Crear usuarios de prueba
    usuarios = [
        Usuario(nombre='Juan Pérez',   email='juan@email.com',   password_hash='hash123', es_profesional=True),
        Usuario(nombre='María García', email='maria@email.com',  password_hash='hash123', es_profesional=True),
        Usuario(nombre='Carlos López', email='carlos@email.com', password_hash='hash123', es_profesional=False),
    ]
    db.session.add_all(usuarios)
    db.session.commit()
    print('✅ Usuarios creados')

    # Crear perfiles profesionales
    profesionales = [
        Profesional(
            usuario_id=1, oficio_id=1,
            descripcion='Plomero con 10 años de experiencia',
            ubicacion='Buenos Aires', telefono='011-1234-5678',
            experiencia_anios=10
        ),
        Profesional(
            usuario_id=2, oficio_id=2,
            descripcion='Electricista matriculada',
            ubicacion='Córdoba', telefono='0351-9876-5432',
            experiencia_anios=5
        ),
    ]
    db.session.add_all(profesionales)
    db.session.commit()
    print('✅ Profesionales creados')

    print('\n🎉 Base de datos lista con datos de prueba!')