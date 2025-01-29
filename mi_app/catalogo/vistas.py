from flask  import request, jsonify, Blueprint
from mi_app import db, login_manager
from mi_app.catalogo.modelos import Product, Category, User, Favorite, Cart, History
from flask import render_template
from flask import flash
from flask import redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import json



'''
prod = {
    "id": 1,
    "nombre": "Grand Theft Auto V",
    "desarrolladora": "Rockstar Games",
    "descripcion": "El juego de hit and run más jugado de la última decada. Controla a Michael, Trevor y Franklin en Los Santos para cometer crímenes o ve al modo online y trolea a los demás jugadores. Saquen GTA 6 Rockstar porfavor",
    "imagen": "GTA5.webp",
    "precio": 39.98,
    "idCategoria": 1,
    "disponibilidad": True,
    "palabrasClave": [
        "Coches",
        "Crimen",
        "disparos"
    ]
}





db.session.add(producto)
db.session.commit()
print("Producto añadido")

'''











@login_manager.user_loader
def load_user(idUsuario):
    return User.query.get(int(idUsuario))

catalog = Blueprint('catalog',__name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    return render_template('home.html')


@catalog.route('/product/<int:id>')
@login_required
def product(id):
    product = Product.query.get_or_404(id)        
    return render_template('producto.html', product=product)


@catalog.route('/products')
def products():
    products = Product.query.all()    
    return render_template('products.html', products=products)



@catalog.route('/products/<int:page>')
@login_required
def productsPag(page=1):
    products = Product.query.paginate(page=page, per_page=3)    
    return render_template('products.html', products=products)


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

    categorias = [
    {
        "nombreCategoria": "Hit and Run"
    },
    {
        "nombreCategoria": "RPG"
    },
    {
        "nombreCategoria": "Supervivencia"
    },
    {
        "nombreCategoria": "Terror Psicológico"
    },
    {
        "nombreCategoria": "Estrategia por turnos"
    },
    {
        "nombreCategoria": "Roguelite"
    },
    {
        "nombreCategoria": "Hack and Slash"
    },
    {
        "nombreCategoria": "Plataformas"
    },
    {
        "nombreCategoria": "Por Turnos"
    },
    {
        "nombreCategoria": "Automatización"
    },
    {
        "nombreCategoria": "Peleas"
    },
    {
        "nombreCategoria": "Metroidvania"
    },
    {
        "nombreCategoria": "Exploración"
    },
    {
        "nombreCategoria": "Puzles"
    },
    {
        "nombreCategoria": "Sigilo"
    },
    {
        "nombreCategoria": "Lore/Historia"
    },
    {
        "nombreCategoria": "Warhammer 40K"
    },
    {
        "nombreCategoria": "Soulslike"
    },
    {
        "nombreCategoria": "FPS"
    }
    ,
    {
        "nombreCategoria": "Acción"
    }
    ,
    {
        "nombreCategoria": "Real Time Strategy"
    }
    ,
    {
        "nombreCategoria": "Vaqueros"
    }
    ]
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