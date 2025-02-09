from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.dialects.postgresql import ARRAY
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'key_dwes_2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://benat:12345678@localhost/TiendaJuegos?port=5432'
db = SQLAlchemy(app)
from  mi_app.tienda.vistas import tienda
app.register_blueprint(tienda)
with app.app_context():
    db.create_all()
