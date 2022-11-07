from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .models import Product
from . import db

views = Blueprint('views', __name__)


@views.route('/home')
@views.route('/')
def home():
    products = Product.query.all()
    return render_template("home1.html", products=products)


@views.route('/products/')
def products():
  
    return render_template("products.html", products=products)


@views.route('/products/<int:id>/')
@login_required
def product(id):
   
    return render_template("/product.html", product=product)


@views.route('/admin/')
@login_required
def admin():
    return render_template("home.html")


@views.route('/admin/products/')
@login_required
def admin_products():

    return render_template("admin/products.html", products=products)


@views.route('/admin/products/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def product_del(id):

    return render_template("/admin/edit-product.html", product=product)


@views.route('/admin/products/<int:id>/', methods=['GET', 'POST'])
@views.route('/admin/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(id):


    return render_template("/admin/edit-product.html", product=product)


@views.route('admin/products/new/', methods=['GET', 'POST'])
@login_required
def new_product():

    return render_template("admin/new-product.html")
