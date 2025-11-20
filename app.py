from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supermercado.db'
app.config['SECRET_KEY'] = 'clave_super_secreta_cambiar_en_produccion'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# Crear directorio de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Modelos de la base de datos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    precio_especial = db.Column(db.Float, nullable=True)
    categoria = db.Column(db.String(50))
    imagen = db.Column(db.String(200), default='default.jpg')
    stock = db.Column(db.Integer, default=0)
    es_especial = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def precio_actual(self):
        return self.precio_especial if self.precio_especial and self.es_especial else self.precio

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)

# Crear tablas y usuario admin por defecto
with app.app_context():
    db.create_all()
    # Crear usuario admin por defecto si no existe
    if not Usuario.query.filter_by(username='admin').first():
        admin_user = Usuario(
            username='admin',
            password=generate_password_hash('admin123'),
            es_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()

# Rutas para clientes
@app.route('/')
def index():
    productos_especiales = Producto.query.filter_by(es_especial=True).limit(8).all()
    categorias = db.session.query(Producto.categoria).distinct().all()
    return render_template('cliente/index.html', 
                         productos=productos_especiales,
                         categorias=[c[0] for c in categorias if c[0]])

@app.route('/productos')
def ver_productos():
    categoria = request.args.get('categoria', '')
    if categoria:
        productos = Producto.query.filter_by(categoria=categoria).all()
    else:
        productos = Producto.query.all()
    
    categorias = db.session.query(Producto.categoria).distinct().all()
    return render_template('cliente/productos.html', 
                         productos=productos, 
                         categoria_actual=categoria,
                         categorias=[c[0] for c in categorias if c[0]])

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
    if query:
        productos = Producto.query.filter(
            Producto.nombre.contains(query) | 
            Producto.descripcion.contains(query)
        ).all()
    else:
        productos = []
    
    categorias = db.session.query(Producto.categoria).distinct().all()
    return render_template('cliente/buscar.html', 
                         productos=productos, 
                         query=query,
                         categorias=[c[0] for c in categorias if c[0]])

@app.route('/producto/<int:id>')
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('cliente/detalle_producto.html', producto=producto)

# Rutas de administración
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.password, password) and usuario.es_admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    total_productos = Producto.query.count()
    productos_especiales = Producto.query.filter_by(es_especial=True).count()
    productos_bajo_stock = Producto.query.filter(Producto.stock < 10).count()
    productos_sin_stock = Producto.query.filter(Producto.stock == 0).count()
    
    return render_template('admin/dashboard.html', 
                         total_productos=total_productos,
                         productos_especiales=productos_especiales,
                         productos_bajo_stock=productos_bajo_stock,
                         productos_sin_stock=productos_sin_stock)

# Gestión de productos
@app.route('/admin/productos')
def admin_productos():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    pagina = request.args.get('pagina', 1, type=int)
    productos = Producto.query.order_by(Producto.fecha_creacion.desc()).paginate(
        page=pagina, per_page=10, error_out=False
    )
    return render_template('admin/productos.html', productos=productos)

@app.route('/admin/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        try:
            es_especial = 'es_especial' in request.form
            precio_especial = float(request.form.get('precio_especial', 0)) if es_especial else None
            
            nuevo_producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                precio_especial=precio_especial,
                categoria=request.form['categoria'],
                stock=int(request.form.get('stock', 0)),
                es_especial=es_especial
            )
            
            # Manejo de imagen (básico)
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen.filename:
                    filename = f"producto_{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
                    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    nuevo_producto.imagen = filename
            
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado exitosamente', 'success')
            return redirect(url_for('admin_productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar producto: {str(e)}', 'error')
    
    categorias = db.session.query(Producto.categoria).distinct().all()
    return render_template('admin/nuevo_producto.html', 
                         categorias=[c[0] for c in categorias if c[0]])

@app.route('/admin/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form['descripcion']
            producto.precio = float(request.form['precio'])
            producto.categoria = request.form['categoria']
            producto.stock = int(request.form.get('stock', 0))
            producto.es_especial = 'es_especial' in request.form
            producto.precio_especial = float(request.form.get('precio_especial', 0)) if producto.es_especial else None
            
            # Manejo de imagen
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen.filename:
                    # Eliminar imagen anterior si no es la default
                    if producto.imagen != 'default.jpg':
                        try:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], producto.imagen))
                        except:
                            pass
                    
                    filename = f"producto_{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
                    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    producto.imagen = filename
            
            db.session.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('admin_productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar producto: {str(e)}', 'error')
    
    categorias = db.session.query(Producto.categoria).distinct().all()
    return render_template('admin/editar_producto.html', 
                         producto=producto,
                         categorias=[c[0] for c in categorias if c[0]])

@app.route('/admin/producto/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    producto = Producto.query.get_or_404(id)
    try:
        # Eliminar imagen si existe
        if producto.imagen and producto.imagen != 'default.jpg':
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], producto.imagen))
            except:
                pass
        
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar producto: {str(e)}', 'error')
    
    return redirect(url_for('admin_productos'))

# Gestión de usuarios
@app.route('/admin/usuarios')
def admin_usuarios():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/admin/usuario/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        try:
            es_admin = 'es_admin' in request.form
            nuevo_usuario = Usuario(
                username=request.form['username'],
                password=generate_password_hash(request.form['password']),
                es_admin=es_admin
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario agregado exitosamente', 'success')
            return redirect(url_for('admin_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar usuario: {str(e)}', 'error')
    
    return render_template('admin/nuevo_usuario.html')

# Ruta para archivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Error handlers
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def error_servidor(error):
    return render_template('errors/500.html'), 500

# Context processor para hacer disponibles algunas variables en todos los templates
@app.context_processor
def inject_variables():
    return dict(
        ahora=datetime.now(),
        categorias=[c[0] for c in db.session.query(Producto.categoria).distinct().all() if c[0]]
    )

if __name__ == '__main__':
    app.run(debug=True)