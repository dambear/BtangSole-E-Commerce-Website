from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash






db = SQLAlchemy()
DB_NAME = "btangsoleShop.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'batangas sole'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
  

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    

    from .models import User
    create_database(app)
    
    createAdmin(app)
    
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


    
    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
            
            
            
            
            
def createAdmin(app):
    
    
    from .models import User

    with app.app_context():
        
        fullname = "Admin"
        email = "admin@admin.com"
        password1 = "admin123"
        admin=True
        address=""
        gender=""
       
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print("Admin exists")
            
        else:
            new_user = User(
                fullname=fullname,
                email=email,
                password=generate_password_hash(password1, method='sha256'),
                is_admin=admin,
                address=address,
                gender=gender,
                
        
            )
            
            db.session.add(new_user)
            db.session.commit()
        
        