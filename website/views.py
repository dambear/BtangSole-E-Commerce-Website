from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .models import Product
from werkzeug.utils import secure_filename
from . import db
import os




views = Blueprint('views', __name__)




@views.route('/home')
@views.route('/')
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)



@views.route('/shop')
def shop():
    products = Product.query.all()
    return render_template("user/shop.html", products=products)


@views.route('/shop/<int:id>/')
@login_required
def product(id):
    product = Product.query.get(id)
    return render_template("user/product-preview.html", product=product)









#------------------------------------------ ADMIN StuFF ------------------------------------------
@views.route('admin')
@login_required
def admin():
    return render_template("admin/admin_home.html")


@views.route('admin/product/')
@login_required
def admin_product():
    return render_template("admin_home.html")




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
        product.image1=request.files.get('image1')
        product.image2=request.files.get('image2')
        product.product_color = request.form.get('product_color')
        product.product_price = request.form.get('product_price')
        product.product_quantity = request.form.get('product_quantity')
        product.image3=request.files.get('image3')
        product.image4=request.files.get('image4')
        
        imagename1 = secure_filename(product.image1.filename)
        imagename2 = secure_filename(product.image2.filename)
        imagename3 = secure_filename(product.image3.filename)
        imagename4 = secure_filename(product.image4.filename)
        
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, app.config['UPLOAD_FOLDER'])
        product.image1.save(os.path.join(upload_path, imagename1))
        product.image2.save(os.path.join(upload_path, imagename2))
        product.image3.save(os.path.join(upload_path, imagename3))
        product.image4.save(os.path.join(upload_path, imagename4))
        
        db.session.commit()

        flash('Product updated successfully!', category='success')
        return redirect(url_for('views.product_edit', id=product.id))

    return render_template("/admin/update_product.html", product=product)



@views.route('admin/products/new/', methods=['GET', 'POST'])
@login_required
def new_product():
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_size = request.form.get('product_size')
        product_description = request.form.get('product_description')
        image1=request.files.get('image1')
        image2=request.files.get('image2')
        product_color = request.form.get('product_color')
        product_price = request.form.get('product_price')
        product_quantity = request.form.get('product_quantity')
        image3=request.files.get('image3')
        image4=request.files.get('image4')
        
        imagename1 = secure_filename(image1.filename)
        imagename2 = secure_filename(image2.filename)
        imagename3 = secure_filename(image3.filename)
        imagename4 = secure_filename(image4.filename)
        
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, app.config['UPLOAD_FOLDER'])
        image1.save(os.path.join(upload_path, imagename1))
        image2.save(os.path.join(upload_path, imagename2))
        image3.save(os.path.join(upload_path, imagename3))
        image4.save(os.path.join(upload_path, imagename4))
        
        
        


        new_product = Product(product_name=product_name, product_size=product_size, 
                              product_description=product_description, 
                              image1=imagename1, image2=imagename2, product_color=product_color, 
                              product_price=product_price, product_quantity=product_quantity, 
                              image3=imagename3, image4=imagename4 )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', category='success')
        product = Product.query.get(new_product.id)
        return redirect(url_for('views.update_product', id=product.id))

    
    return render_template("admin/add_product.html")


