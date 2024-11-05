from flask import Flask, send_file, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
from reportlab.pdfgen import canvas
import io
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'clave_secreta_1234'


import os 
app.config['UPLOAD_FOLDER'] = 'static/image'  
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename

#login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/pruebas_login?charset=utf8mb4&collation=utf8mb4_general_ci'
app.config['SQLALCHEMY_BINDS'] = {
    'tienda_perfumes': 'mysql+mysqlconnector://root:1234@localhost/tienda_perfumes?charset=utf8mb4&collation=utf8mb4_general_ci'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Perfume(db.Model):
    __bind_key__ = 'tienda_perfumes' 
    __tablename__ = 'perfumes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    aroma = db.Column(db.String(50))
    imagen_url = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    precio = db.Column(db.Float)

#----------------------------------------------------------------------- CLASE FACTURA

class Factura(db.Model):
    __bind_key__ = 'tienda_perfumes' 
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, nullable=False)
    tipo_factura = db.Column(db.String(2), nullable=False)
    numero_factura = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    codigo_descripcion = db.Column(db.String(255)) 
    precio_unitario = db.Column(db.Float, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    iva = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.Index('ix_factura_fecha', 'fecha'), 
    )

#-----------------------------------------------------------------------TABLA CLIENTE

class Cliente(db.Model):
    __bind_key__ = 'tienda_perfumes'
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    domicilio = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

def __init__(self, nombre, apellido, localidad, domicilio, codigo_postal, telefono, email):
        self.nombre = nombre
        self.apellido = apellido
        self.localidad = localidad
        self.domicilio = domicilio
        self.codigo_postal = codigo_postal
        self.telefono = telefono
        self.email = email


#-----------------------------------------------------------------------LOGIN USER
# Definimos el modelo para la tabla de admin_users
class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:  # Si no está logueado
            return redirect(url_for('login'))  # Redirigimos al login
        return f(*args, **kwargs)
    return decorated_function

# Ruta para el login
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscamos el usuario en la base de datos
        user = AdminUser.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username  
            return redirect(url_for('home')) 
        else:
            return 'Usuario o contraseña incorrectos'

    return render_template('login.html')

# Ruta para el panel de administrador (protegido)
@app.route('/home')
@login_required
def home():
     return render_template('home.html')
     
# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)  
    return redirect(url_for('login'))

#-----------------------------------------------------------------------GET;POST;PUT;DELETE

@app.route('/ver_catalogo')
@login_required
def ver_catalogo():
    perfumes = Perfume.query.all()
    return render_template('ver_catalogo.html',perfumes=perfumes) 
    
@app.route('/modificar_producto', methods=['GET', 'POST'])
@login_required
def modificar_producto():
    producto = None  

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'buscar':
            producto_id = request.form['producto_id']
            producto = Perfume.query.get(producto_id)
            if not producto:
                flash('Producto no encontrado')  

        elif form_type == 'actualizar':
            producto_id = request.form['producto_id']
            producto = Perfume.query.get(producto_id)

            if producto:
                producto.nombre = request.form['nombre']
                producto.aroma = request.form['aroma']
                producto.imagen_url = request.form['imagen_url']
                producto.stock = request.form['stock']
                producto.precio = request.form['precio']
                db.session.commit()
                flash('Producto actualizado con éxito')
            else:
                flash('Producto no encontrado')  

    return render_template('modificar_producto.html', producto=producto)
   
@app.route('/agregar_producto', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        aroma = request.form['aroma']
        imagen_url = None
        
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen and allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)
                imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(imagen_path) 
                imagen_url = filename  

        stock = request.form['stock']
        precio = request.form['precio']

        
        nuevo_producto = Perfume(
            nombre=nombre,
            aroma=aroma,
            imagen_url=imagen_url,  
            stock=stock,
            precio=precio
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        flash('Producto agregado con éxito')
        return redirect(url_for('agregar_producto')) 

    return render_template('agregar_producto.html')
    
@app.route('/eliminar_producto', methods=['GET', 'POST'])
@login_required
def eliminar_producto():
    producto = None  

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'buscar':
            producto_id = request.form['producto_id']
            producto = Perfume.query.get(producto_id)
            if not producto:
                flash('Producto no encontrado') 

        elif form_type == 'eliminar':
            producto_id = request.form['producto_id']
            producto = Perfume.query.get(producto_id)
            if producto:
                db.session.delete(producto)
                db.session.commit()
                flash('Producto eliminado con éxito')
            else:
                flash('Producto no encontrado para eliminar')

    return render_template('eliminar_producto.html', producto=producto)

@app.route('/ventas_dia', methods=['GET', 'POST'])
@login_required
def ventas_dia():
    if request.method == 'POST':
        fecha = request.form['fecha']
        
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
            ventas = Factura.query.filter(db.func.date(Factura.fecha) == fecha.date()).all()
            
            ventas_detalle = []
            total_dia = 0

            for venta in ventas:
                perfume = Perfume.query.get(venta.pedido_id)  
                if perfume:
                    ventas_detalle.append({
                        'perfume': perfume.nombre,
                        'cantidad': venta.cantidad,
                        'monto': venta.precio_total
                    })
                    total_dia += venta.total  

            return render_template('ventas_dia.html', ventas_detalle=ventas_detalle, total_dia=total_dia)
        except ValueError:
            flash("Formato de fecha inválido")
            return redirect(url_for('ventas_dia'))

    return render_template('ventas_dia_formulario.html')


#-----------------------------------------------------------------------PARTE DEL CLIENTE
#VER CATALOGO
@app.route('/catalogo_cliente')
def catalogo_cliente():
    perfumes = Perfume.query.all()
    carrito_count = session.get('total_items', 0)
    session.modified = True

    return render_template('catalogo_cliente.html', perfumes=perfumes, carrito_count=carrito_count)

#-----------------------------------------------------------------------CARRITO

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    perfume_id = request.form.get('perfume_id')
    cantidad = int(request.form.get('cantidad'))
    if not isinstance(session.get('carrito'), dict):
        session['carrito'] = {}  

    if perfume_id in session['carrito']:
        session['carrito'][perfume_id] += cantidad
    else:
        session['carrito'][perfume_id] = cantidad

    session['total_items'] = sum(session['carrito'].values())

    perfume = Perfume.query.get(int(perfume_id))
    if perfume and perfume.stock >= cantidad:
        perfume.stock -= cantidad  
        db.session.commit() 
        flash('Producto agregado al carrito con éxito!.')
    else:
        flash('No hay suficiente stock para agregar al carrito.')

    session.modified = True  
    return redirect(url_for('catalogo_cliente'))

@app.route('/ver_carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    productos_carrito = []
    total = 0  

    for perfume_id, cantidad in carrito.items():
        perfume = Perfume.query.get(int(perfume_id))  
        if perfume:
            subtotal = perfume.precio * cantidad  
            total += subtotal  
            productos_carrito.append({
                'perfume': perfume,
                'cantidad': cantidad,
                'subtotal': subtotal  
            })

    
    return render_template('ver_carrito.html', productos_carrito=productos_carrito, total=total)

@app.route('/eliminar_del_carrito/<int:perfume_id>', methods=['POST'])
def eliminar_del_carrito(perfume_id):
    carrito = session.get('carrito', {})

    if str(perfume_id) in carrito:
        cantidad = carrito[str(perfume_id)]  
        
        
        perfume = Perfume.query.get(perfume_id)
        if perfume:
            perfume.stock += cantidad 
            db.session.commit()  

        del carrito[str(perfume_id)]
        session['carrito'] = carrito
        
        session['total_items'] = sum(carrito.values())
        session.modified = True
        
        flash('Producto eliminado del carrito y stock actualizado.')
    else:
        flash('El producto no se encontró en el carrito.')

    return redirect(url_for('ver_carrito'))


    carrito = session.get('carrito', {})

    if str(perfume_id) in carrito:
        cantidad = carrito[str(perfume_id)]  
        
        
        perfume = Perfume.query.get(perfume_id)
        if perfume:
            perfume.stock += cantidad 
            db.session.commit()  

        del carrito[str(perfume_id)]
        session['carrito'] = carrito
        
        session['total_items'] = sum(carrito.values())
        session.modified = True
        
        flash('Producto eliminado del carrito y stock actualizado.')
    else:
        flash('El producto no se encontró en el carrito.')

    return redirect(url_for('ver_carrito'))

#-------------------------------------------------------------------PROCESAR PAGO

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    carrito = session.get('carrito', {})
    if not carrito:
        flash("El carrito está vacío.")
        return redirect(url_for('ver_carrito'))

    
    total_compra = 0
    for perfume_id, cantidad in carrito.items():
        perfume = Perfume.query.get(perfume_id)
        if perfume:
            total_compra += perfume.precio * cantidad

    
    session['carrito'] = {}
    session['total_items'] = 0
    session.modified = True

    flash("Pago realizado con éxito. Gracias por tu compra.")
    return redirect(url_for('catalogo_cliente'))

@app.route('/pagar', methods=['POST'])
def pagar():
    flash('Proceso de pago iniciado')

    return redirect(url_for('ver_carrito'))

def generar_pedido_id():
    # Asumiendo que tienes un modelo Pedido que tiene un campo id
    max_pedido = db.session.query(func.max(Pedido.id)).scalar()
    return max_pedido + 1 if max_pedido else 1


def generar_numero_factura():
    # Obtener el máximo número de factura existente, sin el prefijo
    max_factura = db.session.query(func.max(func.cast(func.substr(Factura.numero_factura, 6), db.Integer))).scalar()
    
    # Si no hay facturas, iniciar en 1
    if max_factura is None:
        max_factura = 1
    else:
        max_factura += 1

    # Formatear el número de factura con ceros a la izquierda
    numero_factura = f"0000-{max_factura:08}"
    return numero_factura

@app.route('/datos_cliente', methods=['GET', 'POST'])
def datos_cliente():
    if request.method == 'POST':
        # Recoger datos del cliente
        nuevo_cliente = Cliente(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            localidad=request.form['localidad'],
            domicilio=request.form['domicilio'],
            codigo_postal=request.form['codigo_postal'],
            telefono=request.form['telefono'],
            email=request.form['email']
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        carrito = session.get('carrito', {})
        if not carrito:
            flash("El carrito está vacío.")
            return redirect(url_for('ver_carrito'))

        subtotal = 0
        for perfume_id, cantidad in carrito.items():
            perfume = Perfume.query.get(perfume_id)
            if perfume:
                subtotal += perfume.precio * cantidad

        iva = subtotal * 0.21
        total = subtotal + iva

        nueva_factura = Factura(
            pedido_id=generar_pedido_id(),  # Define esta función si es necesaria
            tipo_factura='A',
            numero_factura=generar_numero_factura(),
            fecha=datetime.now(),
            cantidad=sum(carrito.values()),
            codigo_descripcion="Pedido de perfumes",  
            precio_unitario=subtotal / sum(carrito.values()),  # Ajusta según sea necesario
            precio_total=subtotal,
            subtotal=subtotal,
            iva=iva,
            total=total
        )
        db.session.add(nueva_factura)
        db.session.commit()

        session.pop('carrito', None)

        flash('Compra realizada con éxito. Gracias por tu pedido.')
        return redirect(url_for('descargar_factura', factura_id=nueva_factura.id))

    return render_template('datos_cliente.html')


@app.route('/descargar_factura/<int:factura_id>')
def descargar_factura(factura_id):
    factura = Factura.query.get(factura_id)
    if not factura:
        return "Factura no encontrada", 404  # Manejo de error si la factura no existe
    
    pedido = Pedido.query.get(factura.pedido_id)
    if not pedido:
        return "Pedido no encontrado", 404  # Manejo de error si el pedido no existe
    
    cliente = Cliente.query.get(pedido.cliente_id)  # Asegúrate de usar el campo correcto para el cliente
    if not cliente:
        return "Cliente no encontrado", 404  # Manejo de error si el cliente no existe

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, f"Factura #{factura.numero_factura}")
    c.drawString(100, 730, f"Fecha: {factura.fecha.strftime('%Y-%m-%d')}")
    c.drawString(100, 710, f"Cliente: {cliente.nombre} {cliente.apellido}")
    c.drawString(100, 690, f"Dirección: {cliente.domicilio}, {cliente.localidad}, {cliente.codigo_postal}")
    c.drawString(100, 670, f"Teléfono: {cliente.telefono}")
    c.drawString(100, 650, f"Email: {cliente.email}")

    c.drawString(100, 600, "Detalles de la compra:")
    y_position = 580
    for perfume_id, cantidad in session.get('carrito', {}).items():
        perfume = Perfume.query.get(perfume_id)
        if perfume:
            c.drawString(100, y_position, f"{perfume.nombre} x{cantidad} - ${perfume.precio * cantidad}")
            y_position -= 20

    c.drawString(100, y_position - 20, f"Subtotal: ${factura.subtotal}")
    c.drawString(100, y_position - 40, f"IVA (21%): ${factura.iva}")
    c.drawString(100, y_position - 60, f"Total: ${factura.total}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"factura_{factura.numero_factura}.pdf", mimetype='application/pdf')

#_________________________
if __name__ == '__main__':
    app.run(debug=True)