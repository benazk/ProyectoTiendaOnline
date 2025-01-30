from flask  import request, jsonify, Blueprint
from mi_app import db, login_manager
from mi_app.catalogo.modelos import Product, Category, User, Favorite, Cart, History
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
    return render_template('home.html')  

@catalog.route('/api/productos') # Esta ruta saca los productos de la base de datos y su función devuelve un diccionario en formato JSON
def apiDeProductos():            # Esta ruta la usará vue para hacer un fetch e insertar los datos en el html   
    products = Product.query.all()
    productosDict = {}
    for product in products:
        productosDict[product.idProducto] ={
            "id": product.idProducto,
            "nombre": product.nombre,
            "desarrolladora": product.desarrolladora,
            "descripcion": product.descripcion,
            "imagen": product.imagen,
            "precio": product.precio,
            "idCategoria": product.category_id,
            "disponibilidad": product.disponibilidad,
            "palabrasClave": product.palabrasClave
        }
    print(f"productos conseguidos con api a las: {datetime.now()}")
    return jsonify(productosDict)  
@catalog.route('/api/categorias') 
def apiDeProductos():            
    categorias = Category.query.all()
    categoriasDict = {}
    for categoria in categorias:
        categoriasDict[categoria.idCategoria] ={
            "id": categoria.idCategoria,
            "nombre": categoria.nombre
        }
    return jsonify(categoriasDict)  
@catalog.route('/api/producto/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product)


#@catalog.route('/products')
#def products():
#    products = Product.query.all()    
#    return render_template('products.html', products=products)

@catalog.route('/producto/<int:id>')
def products(id):
    return render_template('product.html')



#@catalog.route('/products/<int:page>')
#@login_required
#def productsPag(page=1):
#    products = Product.query.paginate(page=page, per_page=3)    
#    return render_template('products.html', products=products)


@catalog.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@catalog.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:        
        return redirect(url_for('catalog.home'))
    
    nombre = request.args.get('nombre')
    contrasena = request.args.get('contrasena')
    existing_user = User.query.filter_by(nombre=nombre).first()

    if not (existing_user and existing_user.check_password(contrasena)):
        return render_template('login.html')

    login_user(existing_user, remember=True) #recuerda usuario al cerrar la ventana
    return redirect(url_for('catalog.products'))
    


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
    with open("./mi_app/static/datos/categorias.json") as f:
        categorias = json.load(f)
    for categ in categorias:
        nombre = categ["nombreCategoria"]
        category = Category(nombre)    
        db.session.add(category)
        db.session.commit()
    return render_template('home.html')

@catalog.route('/product-create')
def create_product():
    with open("./mi_app/static/datos/productos.json") as f:
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
        category = Category.query.get(idcategory)  # Assuming you have a Category model defined
        product = Product(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            disponibilidad=disponibilidad,
            desarrolladora=desarrolladora,
            palabrasClave=palabrasClave,
            category=category)    
        db.session.add(product)
        db.session.commit()
    return render_template('home.html')