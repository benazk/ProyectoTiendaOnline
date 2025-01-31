from mi_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#Tabla (N:M) para la relación de Carrito
cart = db.Table('cart',
db.Column('usuario_id', db.Integer, db.ForeignKey('user.idUsuario')),
db.Column('producto_id', db.Integer, db.ForeignKey('product.idProducto')),
db.Column('fechaAgregado', db.DateTime),
db.Column('idCarrito', db.Integer, primary_key=True)
)

#Tabla (N:M) para la relación de Favoritos
favorite = db.Table('favorite',
db.Column('usuario_id', db.Integer, db.ForeignKey('user.idUsuario')),
db.Column('producto_id', db.Integer, db.ForeignKey('product.idProducto')),
db.Column('fechaAgregado', db.DateTime),
db.Column('idFavorito', db.Integer, primary_key=True)
)

#Tabla (N:M) para la relación de Comentarios
comment = db.Table('comment',
db.Column('usuario_id', db.Integer, db.ForeignKey('user.idUsuario')),
db.Column('producto_id', db.Integer, db.ForeignKey('product.idProducto')),
db.Column('comentario', db.String(255)),
)

#Tabla (N:M) para la relación de Comentarios
details = db.Table('details',
db.Column('producto_id', db.Integer, db.ForeignKey('product.idProducto')),
db.Column('compra_id', db.Integer, db.ForeignKey('history.idCompra')),
db.Column('precio', db.Float),
db.Column('idDetalle', db.Integer, primary_key=True)
)

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
    __tablename__ = 'product'  
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    precio = db.Column(db.Float)
    descripcion = db.Column(db.Text)
    disponibilidad = db.Column(db.Boolean) 
    desarrolladora = db.Column(db.String(255))
    palabrasClave = db.Column(db.ARRAY(db.String(255)))

#Cambio nuevo
    destacados = db.Column(db.Boolean)

#Relación con la tabla User y tabla Cart (N:M)
    usuarioRelacionCart = db.relationship('User', secondary=cart, back_populates='productoRelacionCart')

#Relación con la tabla User y tabla Favorite (N:M)
    usuarioRelacionFavorite = db.relationship('User', secondary=favorite, back_populates='productoRelacionFavorite')

#Relación con la tabla User y tabla Favorite (N:M)
    usuarioRelacionComentario = db.relationship('User', secondary=comment, back_populates='productoRelacionComentario')


#Relación con la tabla Historial y tabla Detalles (N:M)
    compraRelacionDetalles = db.relationship('History', secondary=details, back_populates='productoRelacionDetalles')


    category_id = db.Column(db.Integer, db.ForeignKey('category.idCategoria')) #category es el nombre de la tabla en la BD
    #Por defecto, el nombre de la tabla en la BD es el nombre de la clase Category en minísculas.
    category = db.relationship(
        'Category', backref=db.backref('products', lazy='dynamic')
    )

    

    def __init__(self, nombre, precio, descripcion, disponibilidad, desarrolladora, palabrasClave, destacados, category):
        self.nombre = nombre
        self.precio = precio 
        self.descripcion = descripcion
        self.disponibilidad = disponibilidad
        self.desarrolladora = desarrolladora
        self.palabrasClave = palabrasClave
        self.destacados = destacados
        self.category = category

    def __repr__(self):
        return f'<Product {self.idProducto}>'


class History(db.Model, miCRUD):
    __tablename__ = 'history'
    idCompra = db.Column(db.Integer, primary_key=True)
    fechaAgregado = db.Column(db.DateTime)
    #Relación con la tabla User
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.idUsuario'))
    usuario = db.relationship('User', backref=db.backref('compra', lazy='dynamic'))
    
#Relación con la tabla Productos y tabla Detalles (N:M)
    productoRelacionDetalles = db.relationship('Product', secondary=details, back_populates='compraRelacionDetalles')

    def __init__(self, idUsuario, idCompra, fechaAgregado):
        self.idUsuario = idUsuario
        self.idCompra = idCompra
        self.fechaAgregado = fechaAgregado

    def __repr__(self):
        return f'<History {self.idCompra}>'


class User(db.Model, UserMixin, miCRUD):
    __tablename__ = 'user'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    pwdhash = db.Column(db.String())
    correo = db.Column(db.String(100))
#Relación con la tabla Product y tabla Cart (N:M)
    productoRelacionCart = db.relationship('Product', secondary=cart, back_populates='usuarioRelacionCart')
 
 #Relación con la tabla User y tabla Favorite (N:M)
    productoRelacionFavorite = db.relationship('Product', secondary=favorite, back_populates='usuarioRelacionFavorite')

#Relación con la tabla User y tabla Comentario (N:M)
    productoRelacionComentario = db.relationship('Product', secondary=comment, back_populates='usuarioRelacionComentario')


    def __init__(self, nombre, contrasena, correo):
        self.nombre = nombre
        self.pwdhash = generate_password_hash(contrasena)
        self.correo = correo
 
    def check_password(self, contrasena):
        return check_password_hash(self.pwdhash, contrasena)
     
    def __repr__(self):
        return f'<User {self.idUsuario}>'

class Category(db.Model, miCRUD):
    __tablename__ = 'category'
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'<Category {self.idCategoria}>'
    