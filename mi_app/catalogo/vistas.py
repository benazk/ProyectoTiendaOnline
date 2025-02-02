from flask  import request, jsonify, Blueprint
from mi_app import db, login_manager
from mi_app.catalogo.modelos import Product, Category, User, favorite, cart, History, details
from flask import render_template
from flask import flash
from flask import redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import json
from datetime import datetime


@login_manager.user_loader
def load_user(idUsuario):
    return User.query.get(int(idUsuario))

catalog = Blueprint('catalog',__name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    print("esto deberia de ocurrir antes que el fetch (no cap)")
    categorias = Category.query.all()
    destacados = Product.query.all()
    return render_template('index.html', categorias=categorias, destacados=destacados)  
   
@catalog.route('/productos')
@catalog.route('/productos/<int:page>')
def productos(page=1):
    productos = Product.query.paginate(page=page, per_page=12)  
    return render_template('productos.html', productos=productos)
    

@catalog.route('/producto/<int:id>')
def producto(id):
    producto = Product.query.get_or_404(id)
    categoria = Category.query.get_or_404(producto.category_id)
    return render_template('pagina-producto-especifico.html', producto=producto, categoria=categoria)

@catalog.route('/categoria/<int:categ>')
def categoria(categ):
    categoria = Category.query.get_or_404(categ)
    res=[]
    for product in categoria.products:
        res.append({
            'id': product.idProducto,
            'nombre': product.nombre,
            'precio': product.precio,
            'imagen': product.imagen
        })
    return render_template('prods-por-categ.html', res=res, nombreCateg=categoria.nombre)


@catalog.route('/carrito/<string:user>')
def carrito(user):
    return "Carrito de " + user


@catalog.route('/lista-deseados/<string:user>')
def favs(user):
    return "Lista de deseados de " + user


@catalog.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:        
        return redirect(url_for('catalog.home'))
    print("Tierra")
    nombre = request.args.get('nombre')
    contrasena = request.args.get('contrasena')
    existing_user = User.query.filter_by(nombre=nombre).first()

    if not (existing_user and existing_user.check_password(contrasena)):
        return render_template('login.html')
    print("luna", existing_user.idUsuario)
    login_user(existing_user, remember=True) #recuerda usuario al cerrar la ventana
    return redirect(url_for('catalog.home'))
    


@catalog.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('catalog.home'))

    nombre = request.args.get('nombre')
    correo = request.args.get('email')
    contrasena = request.args.get('contrasena')
    if (nombre and contrasena and correo):
        existing_user = User.query.filter_by(nombre=nombre).first()
        if existing_user:            
            return render_template('register.html')
        user = User(nombre, contrasena, correo)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('catalog.login'))
    return render_template('register.html')

    

@catalog.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('catalog.home'))


@catalog.route('/category-create')
def create_category():
    with open("./mi_app/static/datos/categorias.json", encoding='utf-8') as f:
        categorias = json.load(f)
    for categ in categorias:
        nombre = categ["nombreCategoria"]
        category = Category(nombre=nombre)
        db.session.add(category)
        db.session.commit()
    return redirect(url_for('catalog.home'))

@catalog.route('/product-create')
def create_product():
    with open("./mi_app/static/datos/productos.json", encoding='utf-8') as f:
        productos = json.load(f)
        
    for prod in productos:
        nombre = prod["nombre"]
        precio = prod["precio"]
        descripcion = prod["descripcion"]
        imagen = prod["imagen"]
        disponibilidad = prod["disponibilidad"] 
        desarrolladora = prod["desarrolladora"]
        palabrasClave = prod["palabrasClave"]
        idcategory = prod.get("idCategoria")
        destacados = prod["destacado"]
        category = Category.query.get(idcategory)  # Assuming you have a Category model defined
        product = Product(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            destacados=destacados,
            imagen=imagen,
            disponibilidad=disponibilidad,
            desarrolladora=desarrolladora,
            palabrasClave=palabrasClave,
            category=category
        )    
        db.session.add(product)
        db.session.commit()
    return redirect(url_for('catalog.home'))