'''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from  mi_app.catalogo.vistas import catalog
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, ARRAY
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('postgresql://benat:12345678@localhost/prueba?port=5433')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
class Product(Base):
    __tablename__ = 'products'    
    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    precio = Column(Float)
    descripcion = Column(Text)
    disponibilidad = Column(Boolean) 
    desarrolladora = Column(String(255))
    palasbrasClave = Column(ARRAY(String(255)))
Base.metadata.create_all(engine)
    


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


producto = Product(
    idProducto=prod['id'],
    nombre=prod['nombre'],
    precio=prod["precio"],
    descripcion=prod["descripcion"],
    disponibilidad=prod["disponibilidad"],
    desarrolladora=prod["desarrolladora"],
    palasbrasClave=prod["palabrasClave"]
)
session.add(producto)
session.commit()
print("Producto añadido")


'''


