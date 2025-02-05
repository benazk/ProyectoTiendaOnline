from flask  import request, jsonify, Blueprint
from mi_app import db, login_manager
from mi_app.tienda.modelos import Product, Category, User, favorite, cart, History, details, comment
from flask import render_template
from flask import flash
from flask import redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import json
from datetime import datetime
from sqlalchemy import select, column, text, insert, delete



@login_manager.user_loader
def load_user(idUsuario):
    return User.query.get(int(idUsuario))

tienda = Blueprint('tienda',__name__)

@tienda.route('/')
@tienda.route('/home')
def home():
    categorias = Category.query.all()
    destacados = Product.query.all()
    return render_template('index.html', categorias=categorias, destacados=destacados)  


@tienda.route('/productos') # Función para mostrar todos los productos
def productos():
    productos = Product.query.all()  
    return render_template('productos.html', productos=productos)
    

@tienda.route('/producto/<int:id>')  # Función para mostrar un producto (página del producto)
def producto(id):
    producto = Product.query.get_or_404(id)
    categoria = Category.query.get_or_404(producto.category_id)
    existing_prod = False # Esta y la de existing_fav sirven para comprobar si el producto está en la BBDD (si está en favoritos o en el carrito)
    existing_fav = False
    existing_coment = False
    if current_user.is_authenticated: # Solo lo hace si has iniciado sesión
        # Estos dos stmt son queries de sqlalchemy puro, porque cart y favorito al se tablas N:M, esta es la manera de hacer queries
        stmt = select(column("idUsuario"), column("idProducto"), column("fechaAgregado"), column("idCarrito")).select_from(cart).where(column("idUsuario") == current_user.idUsuario).where(column("idProducto") == id)
        stmt2 = select(column("idUsuario"), column("idProducto"), column("fechaAgregado"), column("idFavorito")).select_from(favorite).where(column("idUsuario") == current_user.idUsuario).where(column("idProducto") == id)
        stmt3 = select(column("usuario_id"), column("producto_id"), column("comentario")).select_from(comment).where(column("producto_id") == id)
        existing_prod = db.session.execute(stmt).fetchone() # El .fecthone() equivale al .first()
        existing_fav = db.session.execute(stmt2).fetchone()      
        resultados = db.session.execute(stmt3).fetchall()
        existing_coment = [tuple(row) for row in resultados]
        comentarios = []
        for p in existing_coment:
            busqueda = User.query.get_or_404(p[0])
            comentarios.append({
                'usuario': busqueda.nombre,
                'comentario': p[2]
            })

    return render_template('pagina-producto-especifico.html', producto=producto, categoria=categoria, existing_prod=existing_prod, existing_fav=existing_fav, comentarios=comentarios)


@tienda.route('/anadirComentario/<int:id>')
def anadirComentario(id):
    print(current_user.idUsuario)
    stmt = insert(comment).values(
        usuario_id = current_user.idUsuario,
        producto_id = id,
        comentario = request.args.get('comentario')  
    )
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for('tienda.producto', id=id))
    

@tienda.route('/categoria/<int:categ>') # Función para mostrar todos los productos de X categoría
def categoria(categ):
    categoria = Category.query.get_or_404(categ)
    res=[] # Para guardar los productos de dicha categoría
    for product in categoria.products: # El categoría.products es una relación especial que facilita buscar los productos por categoría
        res.append({
            'id': product.idProducto,
            'nombre': product.nombre,
            'precio': product.precio,
            'imagen': product.imagen
        })
    return render_template('prods-por-categ.html', res=res, nombreCateg=categoria.nombre)

@tienda.route('/addcart/<int:idUser>/<int:idProd>') # Se le llama desde la página de productos específicos al darle a añadir al carrito
@login_required # La función solo se ejecutará si el usuario ha iniciado sesión
def add_carrito(idUser, idProd):
    horaAnadido = datetime.today().strftime('%Y-%m-%d %H:%M') # Registrar la hora en la que el producto se ha añadido
    stmt = insert(cart).values( # Un insert de sqlalchemy puro por lo de las tablas N:M
        idUsuario=idUser,
        idProducto=idProd,
        fechaAgregado=horaAnadido
    )
    db.session.execute(stmt)
    db.session.commit() # Hacer commit al final
    return redirect(url_for('tienda.producto', id=idProd)) # Redirigir a la página del producto

@tienda.route('/getcarrito/<string:user>') # Esta función de ruta getcarrito con el nombre de usuario hace una query, la convierte en diccionario y se la pasa a VUE a través del return 
@login_required
def getcarrito(user):
    stmt = select(column("idUsuario"), column("idProducto"), column("fechaAgregado"), column("idCarrito")).select_from(cart).where(column("idUsuario") == current_user.idUsuario)
    results = db.session.execute(stmt).fetchall() # el .fetchall() equivale a el .query.all()
    prods_carrito = [tuple(row) for row in results] # tengo que transformar el formato de la query de sqlalchemy a tuplas
    prod = []
    for p in prods_carrito:
        print(p[1])
        prods = Product.query.get_or_404(p[1])
        prod.append({
            'id': prods.idProducto,
            'nombre': prods.nombre,
            'precio': prods.precio,
            'imagen': prods.imagen,
            'idUsuario': p[0],
            'hora': p[2],
            'nombreUsuario': current_user.nombre
        })
    return jsonify(prod) # Lo que devuelve es un diccionario con los productos en el carrito


@tienda.route('/carrito/<string:user>')
@login_required
def carrito(user):
    return render_template("carrito.html")

@tienda.route('/deletecarrito/<int:idUser>/<int:idProd>') # Elimina un producto del carrito
@login_required
def deletecarrito(idUser, idProd):
    stmt = delete(cart).where(column("idUsuario") == current_user.idUsuario, column("idProducto") == idProd) # Query de sqlalchemy
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for('tienda.carrito', user="benat")) # Redirección al carrito al eliminar el producto

# Las siguientes funciones son iguales que la del carrito, no es necesario comentar
@tienda.route('/addfavs/<int:idUser>/<int:idProd>') 
@login_required
def add_favs(idUser, idProd):
    horaAnadido = datetime.today().strftime('%Y-%m-%d %H:%M')
    print(favorite.columns.keys())
    stmt = insert(favorite).values(
        idUsuario=idUser,
        idProducto=idProd,
        fechaAgregado=horaAnadido
    )
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for('tienda.producto', id=idProd))

@tienda.route('/favs/<string:user>')
@login_required
def getfavs(user):
    stmt = select(column("idUsuario"), column("idProducto"), column("fechaAgregado"), column("idFavorito")).select_from(favorite).where(column("idUsuario") == current_user.idUsuario)
    results = db.session.execute(stmt).fetchall()
    prods_favs = [tuple(row) for row in results]
    prod = []
    for f in prods_favs:
        print(p[1])
        favs = Product.query.get_or_404(p[1])
        prod.append({
            'id': favs.idProducto,
            'nombre': favs.nombre,
            'precio': favs.precio,
            'imagen': favs.imagen,
            'hora': p[2],
            'nombreUsuario': current_user.nombre
        })
    return render_template("favoritos.html", )


@tienda.route('/lista-deseados/<string:user>')
@login_required
def favs(user):
    stmt = select(column("idUsuario"), column("idProducto"), column("fechaAgregado"), column("idFavorito")).select_from(favorite).where(column("idUsuario") == current_user.idUsuario)
    results = db.session.execute(stmt).fetchall()
    prods_favs = [tuple(row) for row in results]
    fav = []
    for f in prods_favs:
        favs = Product.query.get_or_404(f[1])
        fav.append({
            'id': favs.idProducto,
            'nombre': favs.nombre,
            'precio': favs.precio,
            'imagen': favs.imagen,
            'hora': f[2],
            'nombreUsuario': current_user.nombre
        })
    return render_template("favoritos.html", idUser=current_user.idUsuario, favs=fav)

@tienda.route('/deletefavs/<int:idUser>/<int:idProd>')
@login_required
def deletefavs(idUser, idProd):
    stmt = delete(favorite).where(column("idUsuario") == current_user.idUsuario, column("idProducto") == idProd)
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for('tienda.favs', user=current_user.nombre))
## Fin de las funciones parecidas a las del carrito


@tienda.route('/buscar-query', methods=['GET', 'POST']) # Para buscar productos con la barra de busqueda
def query():
    query = request.args.get('query')
    productos = Product.query.all()
    prod_filtered = []
    for prod in productos:
        c = [p.lower() for p in prod.palabrasClave] # Esto convierte todos los items del array de palabras clave a minusculas
        if str(query).lower() in str(prod.nombre).lower(): # Si la palabra escrita está en el titulo del producto añade un producto al array de productos a mostrar
            prod_filtered.append({
                "idProducto":prod.idProducto,
                "nombre":prod.nombre,
                "imagen":prod.imagen,
                "precio":prod.precio
            })
        elif str(query) in c: # c siendo el array de palabras clave, compara lo buscado por el usuario y si coincide lo inserta en el array
            prod_filtered.append({
                "idProducto":prod.idProducto,
                "nombre":prod.nombre,
                "imagen":prod.imagen,
                "precio":prod.precio
            })
    return render_template("productos.html", productos=prod_filtered)

@tienda.route('/login', methods=['GET', 'POST']) ## Función para iniciar sesión
def login():
    if current_user.is_authenticated:        
        return redirect(url_for('tienda.home'))
    nombre = request.args.get('nombre')
    contrasena = request.args.get('contrasena')
    existing_user = User.query.filter_by(nombre=nombre).first()

    if not (existing_user and existing_user.check_password(contrasena)):
        return render_template('login.html')
    login_user(existing_user, remember=True) #recuerda usuario al cerrar la ventana
    return redirect(url_for('tienda.home'))
    

@tienda.route('/registerform')
def registerform():
    return render_template('register.html')

@tienda.route('/register', methods=['GET', 'POST']) ## Función para crear cuenta
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tienda.home'))

    nombre = request.args.get('nombre')
    correo = request.args.get('email')
    contrasena = request.args.get('contrasena')
    print(f"nombre de usuario: {nombre}")
    if (nombre and contrasena and correo):
        existing_user = User.query.filter_by(nombre=nombre).first()
        if existing_user:            
            return render_template('register.html')
        user = User(nombre, contrasena, correo)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('tienda.login'))
    return render_template('index.html')

    

@tienda.route('/logout') ## Función para cerrar sesión
@login_required
def logout():
    logout_user()
    return redirect(url_for('tienda.home'))


@tienda.route('/category-create') ## Función para crear las categorías (solo para los desarrolladores)
def create_category():
    with open("./mi_app/static/datos/categorias.json", encoding='utf-8') as f:
        categorias = json.load(f)
    for categ in categorias:
        nombre = categ["nombreCategoria"]
        category = Category(nombre=nombre)
        db.session.add(category)
        db.session.commit()
    return redirect(url_for('tienda.home'))

@tienda.route('/product-create') ## Función para crear los productos (solo para los desarrolladores)
def create_product():
    with open("./mi_app/static/datos/productos.json", encoding='utf-8') as f:
        productos = json.load(f)
        
    for prod in productos:
        nombre = prod["nombre"]
        precio = prod["precio"]
        descripcion = prod["descripcion"]
        imagen = prod["imagen"]
        imagenBig = prod["imagenBig"]
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
            imagenBig=imagenBig,
            disponibilidad=disponibilidad,
            desarrolladora=desarrolladora,
            palabrasClave=palabrasClave,
            category=category
        )    
        db.session.add(product)
        db.session.commit()
    return redirect(url_for('tienda.home'))