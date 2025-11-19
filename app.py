from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Archivo donde guardaremos los artículos
ARTICLES_FILE = 'data/articulos.json'

def cargar_articulos():
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_articulos(articulos):
    # Crear directorio si no existe
    os.makedirs('data', exist_ok=True)
    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(articulos, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    articulos = cargar_articulos()
    return render_template('index.html', articulos=articulos)

@app.route('/articulo/<int:articulo_id>')
def ver_articulo(articulo_id):
    articulos = cargar_articulos()
    articulo = next((a for a in articulos if a['id'] == articulo_id), None)
    if articulo:
        return render_template('articulo.html', articulo=articulo)
    return "Artículo no encontrado", 404

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Agregar nuevo artículo
        articulos = cargar_articulos()
        
        nuevo_articulo = {
            'id': len(articulos) + 1,
            'titulo': request.form['titulo'],
            'contenido': request.form['contenido'],
            'autor': request.form['autor'],
            'fecha': request.form['fecha'],
            'categoria': request.form['categoria'],
            'imagen': request.form['imagen'] or '/static/images/default.jpg'
        }
        
        articulos.append(nuevo_articulo)
        guardar_articulos(articulos)
        return redirect(url_for('admin'))
    
    articulos = cargar_articulos()
    return render_template('admin.html', articulos=articulos)

@app.route('/eliminar/<int:articulo_id>')
def eliminar_articulo(articulo_id):
    articulos = cargar_articulos()
    articulos = [a for a in articulos if a['id'] != articulo_id]
    guardar_articulos(articulos)
    return redirect(url_for('admin'))

@app.route('/editar/<int:articulo_id>', methods=['GET', 'POST'])
def editar_articulo(articulo_id):
    articulos = cargar_articulos()
    articulo = next((a for a in articulos if a['id'] == articulo_id), None)
    
    if not articulo:
        return "Artículo no encontrado", 404
    
    if request.method == 'POST':
        # Actualizar artículo
        articulo['titulo'] = request.form['titulo']
        articulo['contenido'] = request.form['contenido']
        articulo['autor'] = request.form['autor']
        articulo['fecha'] = request.form['fecha']
        articulo['categoria'] = request.form['categoria']
        articulo['imagen'] = request.form['imagen']
        
        guardar_articulos(articulos)
        return redirect(url_for('admin'))
    
    return render_template('editar.html', articulo=articulo)

if __name__ == '__main__':
    app.run(debug=True)