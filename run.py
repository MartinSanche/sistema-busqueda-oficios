# run.py
from app import create_app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    print('🚀 Iniciando el servidor...')
    print('📍 Abrí tu navegador en: http://localhost:5000')
    app.run(debug=True)