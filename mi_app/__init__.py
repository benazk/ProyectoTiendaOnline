from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from  mi_app.catalogo.vistas import catalog
from flask_login import LoginManager
from sqlalchemy.dialects.postgresql import ARRAY
# si lo pongo aquí me da un problema de importación circular
# ImportError: cannot import name 'db' from partially 
# #initialized module 'mi_app' (most likely due to a circular 
# import). Normal, en vistas se hace import db, todavía no creado.

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'key_dwes_2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bryanBlu:bryan007@localhost/Juegos2?port=5433'
db = SQLAlchemy(app)
from  mi_app.catalogo.vistas import catalog
app.register_blueprint(catalog)
with app.app_context():
    db.create_all()

@app.template_filter('decode_utf8')
def decode_utf8(value):
    #try:
    return value.decode('UTF-8')
    #except AttributeError:
    #    print("no se ha podido decodificar")
    #    return value

# Register the filter
app.jinja_env.filters['decode_utf8'] = decode_utf8