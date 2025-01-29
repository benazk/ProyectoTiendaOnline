from mi_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class miCRUD:
    def create(self, session):
        session.add(self)
        session.commit()

    @classmethod
    def read(cls, session, **consulta):
        return session.query(cls).filter_by(**consulta).all() #devuelve una lista de objetos
        #return session.query(cls).all()
    
    @classmethod  #Método para devolver los 20
    def read_last_20(cls, session):
        return session.query(cls).order_by(cls.id.desc()).limit(10).all()

    def update(self,session):
        session.commit()
    def delete(self, session):
        
        session.delete(self)
        session.commit()



class Product(db.Model, miCRUD):    
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    precio = db.Column(db.Float)
    descripcion = db.Column(db.Text)
    disponibilidad = db.Column(db.Boolean) 
    desarrolladora = db.Column(db.String(255))
    palabrasClave = db.Column(db.ARRAY(db.String(255)))
    category_id = db.Column(db.Integer, db.ForeignKey('category.idCategoria')) #category es el nombre de la tabla en la BD
    #Por defecto, el nombre de la tabla en la BD es el nombre de la clase Category en minísculas.
    category = db.relationship(
        'Category', backref=db.backref('products', lazy='dynamic')
    )

    

    def __init__(self, nombre, precio, descripcion, disponibilidad, desarrolladora, palabrasClave, category):
        self.nombre = nombre
        self.precio = precio 
        self.descripcion = descripcion
        self.disponibilidad = disponibilidad
        self.desarrolladora = desarrolladora
        self.palabrasClave = palabrasClave
        self.category = category

    def __repr__(self):
        return f'<Product {self.idProducto}>'

class Category(db.Model, miCRUD):
    # __tablename__ = 'category'  es el nombre que le da flask por defecto a la tabla de la BD
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'<Category {self.idCategoria}>'


class User(db.Model, UserMixin, miCRUD):
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    pwdhash = db.Column(db.String())
    correo = db.Column(db.String(100))
 
    def __init__(self, nombre, contrasena, correo):
        self.nombre = nombre
        self.pwdhash = generate_password_hash(contrasena)
        self.correo = correo
 
    def check_password(self, contrasena):
        return check_password_hash(self.pwdhash, contrasena)
     
    def __repr__(self):
        return f'<User {self.idUsuario}>'

class Cart(db.Model, miCRUD):
    idCarrito = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('user.idUsuario'))
    idProducto = db.Column(db.Integer, db.ForeignKey('product.idProducto'))
    fechaAgregado = db.Column(db.DateTime)


    def __init__(self, idUsuario, idProducto, fechaAgregado):
        self.idUsuario = idUsuario
        self.idProducto = idProducto
        self.fechaAgregado = fechaAgregado
  
    def __repr__(self):
        return f'<Car {self.idCarrito}>'
    
class Favorite(db.Model, miCRUD):
    idFavorito = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('user.idUsuario'))
    idProducto = db.Column(db.Integer, db.ForeignKey('product.idProducto'))
    fechaAgregado = db.Column(db.DateTime)

    def __init__(self, idUsuario, idProducto, fechaAgregado):
        self.idUsuario = idUsuario
        self.idProducto = idProducto
        self.fechaAgregado = fechaAgregado

    def __repr__(self):
        return f'<Favorite {self.idFavorito}>'

class History(db.Model, miCRUD):
    idCompra = db.Column(db.Integer, primary_key=True)
    idCarrito = db.Column(db.Integer, db.ForeignKey('cart.idCarrito'))
    idUsuario = db.Column(db.Integer, db.ForeignKey('user.idUsuario'))
    idProducto = db.Column(db.Integer, db.ForeignKey('product.idProducto'))
    fechaAgregado = db.Column(db.DateTime)

    def __init__(self, idCarrito, idUsuario, idProducto, fechaAgregado):
        self.idCarrito = idCarrito
        self.idUsuario = idUsuario
        self.idProducto = idProducto
        self.fechaAgregado = fechaAgregado

    def __repr__(self):
        return f'<History {self.idCompra}>'
    