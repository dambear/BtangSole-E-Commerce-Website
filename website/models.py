from . import db
from flask_login import UserMixin


#----------User Tab;e-----------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False)
    join_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    
    

        
    
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    product_size = db.Column(db.String(500))
    product_description = db.Column(db.String(3000))
    image1 = db.Column(db.String(1000))
    image2 = db.Column(db.String(1000))
    product_color = db.Column(db.String(2000))
    product_price = db.Column(db.Integer)
    product_quantity = db.Column(db.Float)
    image3 = db.Column(db.String(1000))
    image4 = db.Column(db.String(1000))
    date_added = db.Column(db.DateTime(timezone=True), default=db.func.now())

