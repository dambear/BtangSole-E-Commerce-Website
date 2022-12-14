from . import db
from flask_login import UserMixin


#----------User Tab;e-----------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(1500))
    gender = db.Column(db.String(30))
    birthday = db.Column(db.DateTime)
    join_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    
    
    

        
    
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    product_size = db.Column(db.String(500))
    product_description = db.Column(db.String(3000))
    image1 = db.Column(db.String(1000))
    image2 = db.Column(db.String(1000))
    product_color = db.Column(db.String(1000))
    product_price = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)
    product_category = db.Column(db.String(100))
    image3 = db.Column(db.String(1000))
    image4 = db.Column(db.String(1000))
    date_added = db.Column(db.DateTime(timezone=True), default=db.func.now())


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image1 = db.Column(db.String(1000))
    product_name = db.Column(db.String(150))
    product_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Integer)
    
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    mobilenum = db.Column(db.String(11))
    address = db.Column(db.String(700))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(150))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    paymentmethod = db.Column(db.String(150))
    approve = db.Column(db.Boolean, default=False)