from . import db
from flask_login import UserMixin


#----------User Tab;e-----------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(80))

    
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(80))




#----------Product Table-----------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    description = db.Column(db.String(3200))
    image = db.Column(db.String(255))
    category = db.Column(db.String(150))
    stock = db.Column(db.Integer)
    rating = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), default=db.func.now())
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    
#----------Item Table-----------
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    description = db.Column(db.String(3200))
    image = db.Column(db.String(255))
    category = db.Column(db.String(150))
    stock = db.Column(db.Integer)
    rating = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), default=db.func.now())


