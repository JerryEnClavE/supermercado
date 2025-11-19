from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_simple'  # Necesaria para sesiones

# Archivo donde guardaremos los artículos
ARTICLES_FILE = 'articulos.json'

@app.context_processor
def inject_user():
    return {'usuario_actual': session.get('usuario')}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['usuario'] = request.form.get('usuario')
        return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

def cargar_articulos():
    """Cargar artículos desde el archivo JSON"""
    try:
        if os.path.exists(ARTICLES_FILE):
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error cargando artículos: {e}")
    return []

def guardar_articulos(articulos):
    """Guardar artículos en el archivo JSON"""
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articulos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando artículos: {e}")

@app.route('/')
def index():
    """Página principal con todos los artículos"""
    articulos = cargar_articulos()
    return render_template('index.html', articulos=articulos)

@app.route('/articulo/<int:articulo_id>')
def ver_articulo(articulo_id):
    """Página individual de un artículo"""
    articulos = cargar_articulos()
    articulo = next((a for a in articulos if a['id'] == articulo_id), None)
    if articulo:
        return render_template('articulo.html', articulo=articulo)
    return "Artículo no encontrado", 404

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Página de administración para crear/editar artículos (productos)"""
    if request.method == 'POST':
        articulos = cargar_articulos()
        nuevo_articulo = {
            'id': len(articulos) + 1,
            'nombre': request.form['nombre'],
            'precio': float(request.form.get('precio', 0)),
            'autor': session.get('usuario', request.form.get('autor', 'Administrador'))
        }
        articulos.append(nuevo_articulo)
        guardar_articulos(articulos)
        return redirect(url_for('admin'))
    articulos = cargar_articulos()
    return render_template('admin.html', articulos=articulos)

@app.route('/eliminar/<int:articulo_id>')
def eliminar_articulo(articulo_id):
    """Eliminar un artículo"""
    articulos = cargar_articulos()
    articulo = next((a for a in articulos if a['id'] == articulo_id), None)
    if not articulo:
        return "Artículo no encontrado", 404
    if articulo.get('autor') != session.get('usuario'):
        return "No autorizado", 403
    articulos = [a for a in articulos if a['id'] != articulo_id]
    guardar_articulos(articulos)
    return redirect(url_for('admin'))

@app.route('/editar/<int:articulo_id>', methods=['GET', 'POST'])
def editar_articulo(articulo_id):
    """Editar un artículo existente"""
    articulos = cargar_articulos()
    articulo = next((a for a in articulos if a['id'] == articulo_id), None)
    if not articulo:
        return "Artículo no encontrado", 404
    if articulo.get('autor') != session.get('usuario'):
        return "No autorizado", 403
    if request.method == 'POST':
        articulo['nombre'] = request.form['nombre']
        articulo['precio'] = float(request.form.get('precio', 0))
        guardar_articulos(articulos)
        return redirect(url_for('admin'))
    return render_template('editar.html', articulo=articulo)

# Crear algunos datos de ejemplo si no existen
def crear_datos_ejemplo():
    articulos = cargar_articulos()
    if not articulos:
        articulos_ejemplo = [
            {
                'id': 1,
                'titulo': 'Bienvenido a Mi Revista',
                'contenido': 'Esta es una revista simple creada con Flask. Puedes editar, crear y eliminar artículos fácilmente.',
                'autor': 'Administrador',
                'fecha': '2024-01-01',
                'categoria': 'General',
                'imagen': 'https://via.placeholder.com/400x200?text=Imagen+Ejemplo'
            },
            {
                'id': 2,
                'titulo': 'Cómo Usar Esta Revista',
                'contenido': 'Ve a la página de Editor para crear nuevos artículos. Puedes editar o eliminar los existentes fácilmente.',
                'autor': 'Administrador',
                'fecha': '2024-01-01',
                'categoria': 'Tutorial',
                'imagen': 'https://via.placeholder.com/400x200?text=Tutorial'
            }
        ]
        guardar_articulos(articulos_ejemplo)

if __name__ == '__main__':
    crear_datos_ejemplo()
    app.run(debug=True)