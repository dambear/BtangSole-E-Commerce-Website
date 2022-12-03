from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .models import Product, Cart, Order
from werkzeug.utils import secure_filename
from . import db
import os




views = Blueprint('views', __name__)


app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



@views.route('/home')
@views.route('/')
def home():
    category="Featured"
    products = Product.query.filter_by(product_category=category)
    return render_template("home.html", products=products)



@views.route('/shop')
def shop():
    products = Product.query.all()
    return render_template("user/shop.html", products=products)


@views.route('/shop/<int:id>/', methods=['GET', 'POST'])
@login_required
def product(id):
    product = Product.query.get(id)
    
    
    if request.method == 'POST':
        
        
        
        
        existingincart = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()
        
        if existingincart:
            flash('Same product is already in cart!', category='error')
        
        else:
            quantity = 1
            
            
            
            total = quantity*product.product_price

            add_to_cart = Cart(user_id=current_user.id, product_id=product.id, 
                            image1=product.image1, product_name=product.product_name,  
                            product_price=product.product_price, quantity=quantity, total=total)
                
            db.session.add(add_to_cart)
            db.session.commit()
            flash('Product added to cart successfully!', category='success')
      
        
        
            
    
    
    
    return render_template("user/shop-item-preview.html", product=product)



@views.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    
    carts = Cart.query.filter_by(user_id=current_user.id)
    
    
    cart_total = []
    for cart_t in carts:
        i = cart_t.total
        cart_total.insert(0,i)
        
    cart_total = sum(cart_total)
    shippingfee = 100
    
    order_total = cart_total+ shippingfee
    
    if request.method == 'POST':
        

    
        if request.form.get('plus') == '+':
            

            
            cid = request.form.get('cid')
            carts = Cart.query.get(cid)
        
        
            carts.quantity = carts.quantity + 1
            db.session.commit()
            
            carts.total = carts.quantity*carts.product_price
            
            db.session.commit()
    
            return redirect(url_for('views.cart'))
        
        if request.form.get('minus') == '-':
            

            
            cid = request.form.get('cid')
            carts = Cart.query.get(cid)
        

                

                    
            carts.quantity = carts.quantity - 1
            db.session.commit()
                
            carts.total = carts.quantity*carts.product_price
                
            db.session.commit()
    
            return redirect(url_for('views.cart'))
            
            
            
        if request.form.get('delete') == 'delete':
             
            cid = request.form.get('cid')
            carts = Cart.query.get(cid)
            
                    
            db.session.delete(carts)
            db.session.commit()
            
            return redirect(url_for('views.cart'))
        
        if request.form.get('checkout') == 'checkout':
            
            return redirect(url_for('views.order_checkout'))
            
    
    return render_template("user/cart.html", carts=carts, cart_total=cart_total, order_total=order_total)




@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def order_checkout():
    
    carts = Cart.query.filter_by(user_id=current_user.id)
    
   
    
    
    cart_total = []
    for cart_t in carts:
        i = cart_t.total
        cart_total.insert(0,i)
        
    cart_total = sum(cart_total)
    shippingfee = 100
    
    order_total = cart_total+ shippingfee
    
    
    if request.method == 'POST':
        
        cid = request.form.get('cid')
        
        cart = Cart.query.get(cid)
        
        
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        pnumber = request.form.get('pnumber')
        province_text = request.form.get('province_text')
        city_text = request.form.get('city_text')
        barangay_text = request.form.get('barangay_text')
        street_text = request.form.get('street_text')
        paymentmethod = request.form.get('paymentmethod')
        
        address = province_text + ", " + city_text + ", " + barangay_text + ", " + street_text
        
        fullname = fname + " " + lname
        
        
        add_to_order = Order(fullname=fullname, mobilenum=pnumber, address=address,  
                            product_id=cart.product_id, product_name=cart.product_name, 
                            quantity=cart.quantity, total_price=order_total, 
                            paymentmethod=paymentmethod)
        
        db.session.add(add_to_order)
        db.session.commit()
        
        flash('Your Order was successfully place!', category='success')
        
        
        product = Product.query.get(cart.product_id)
        
        
    
        product.product_quantity = product.product_quantity - cart.quantity
        
        db.session.commit()
        
        
        cartdelete = Cart.query.get(cid)
        
        db.session.delete(cartdelete)
        db.session.commit()
        
        return redirect(url_for('views.home'))
    
    
    

    return render_template("user/checkout.html", carts=carts, cart_total=cart_total, order_total=order_total)





#------------------------------------------ ADMIN StuFF ------------------------------------------
@views.route('/admin')
@login_required
def admin():
    return render_template("admin/admin_home.html")

@views.route('/admin/order-table')
@login_required
def admin_orders():
    orders = Order.query.all()
    return render_template("admin/admin_order_table.html", orders=orders)



@views.route('/admin/product-table')
@login_required
def admin_products():
    products = Product.query.all()
    return render_template("admin/admin_product_table.html", products=products)


@views.route('/admin/products/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def product_del(id):
    product = Product.query.get(id)
    if not product:
        flash('Product not found.', category='error')
        return redirect(url_for('views.admin_products'))

    if request.method == 'POST':
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()

    product = Product.query.get(id)
    return render_template("/admin/update_product.html", product=product)



@views.route('/admin/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def update_product(id):
    product = Product.query.get(id)
    if not product:
        flash('Product not found.', category='error')
        return redirect(url_for('views.admin'))

    if request.method == 'POST':
        product = Product.query.get(id)
        product.product_name = request.form.get('product_name')
        product.product_size = request.form.get('product_size')
        product.product_description = request.form.get('product_description')
        image1=request.files.get('image1')
        image2=request.files.get('image2')
        product.product_color = request.form.get('product_color')
        product.product_price = request.form.get('product_price')
        product.product_quantity = request.form.get('product_quantity')
        product.product_category = request.form.get('category')
        image3=request.files.get('image3')
        image4=request.files.get('image4')
        

        
            
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, app.config['UPLOAD_FOLDER'])
        
        
        
        if request.files['image1'].filename == '':
            product.image1 = product.image1 
            
        else:
            imagename1 = secure_filename(image1.filename)
            image1.save(os.path.join(upload_path, imagename1))
            product.image1 = imagename1
            
        if request.files['image2'].filename == '':
            product.image2 =  product.image2 
            
        else:
            imagename2 = secure_filename(image2.filename)
            image2.save(os.path.join(upload_path, imagename2))
            product.image2 = imagename2
            
            
        if request.files['image3'].filename == '':
            product.image3 = product.image3 
            
            
        else:
            imagename3 = secure_filename(image3.filename)
            image3.save(os.path.join(upload_path, imagename3))
            product.image3 = imagename3
            
            
        if request.files['image4'].filename == '':
            product.image4 = product.image4
            
        else:
            imagename4 = secure_filename(image4.filename)
            image4.save(os.path.join(upload_path, imagename4))
            product.image4 = imagename4
            

        
 
        db.session.commit()
        

        flash('Product updated successfully!', category='success')
        return redirect(url_for('views.update_product', id = product.id))

    return render_template("/admin/update_product.html", product=product)



@views.route('admin/products/new/', methods=['GET', 'POST'])
@login_required
def add_product():
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_size = request.form.get('product_size')
        product_description = request.form.get('product_description')
        image1=request.files.get('image1')
        image2=request.files.get('image2')
        product_color = request.form.get('product_color')
        product_price = request.form.get('product_price')
        product_quantity = request.form.get('product_quantity')
        product_category = request.form.get('category')
        image3=request.files.get('image3')
        image4=request.files.get('image4')
        
        
        
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, app.config['UPLOAD_FOLDER'])
       
       
        if request.files['image1'].filename == '':
            flash('Image 1 cannot be empty!', category='success')
            
        else:
            imagename1 = secure_filename(image1.filename)
            image1.save(os.path.join(upload_path, imagename1))
            
        if request.files['image2'].filename == '':
            imagename2 = "ifnoimageenteredshowthis.jpg"
            
        else:
            imagename2 = secure_filename(image2.filename)
            image2.save(os.path.join(upload_path, imagename2))
            
            
        if request.files['image3'].filename == '':
            imagename3 = "ifnoimageenteredshowthis.jpg"
            
        else:
            imagename3 = secure_filename(image3.filename)
            image3.save(os.path.join(upload_path, imagename3))
            
            
        if request.files['image4'].filename == '':
            imagename4 = "ifnoimageenteredshowthis.jpg"
            
        else:
            imagename4 = secure_filename(image4.filename)
            image4.save(os.path.join(upload_path, imagename4))
            
        
        


        new_product = Product(product_name=product_name, product_size=product_size, 
                              product_description=product_description, 
                              image1=imagename1, image2=imagename2, product_color=product_color, 
                              product_price=product_price, product_quantity=product_quantity, 
                              product_category=product_category,image3=imagename3, image4=imagename4 )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', category='success')
        product = Product.query.get(new_product.id)
        return redirect(url_for('views.update_product', id=product.id))

    
    return render_template("admin/admin_add_product.html")


