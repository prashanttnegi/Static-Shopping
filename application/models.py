from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    email_id=db.Column(db.String,unique=True, nullable=False)
    password=db.Column(db.String,nullable=False)
    active=db.Column(db.Boolean)
    
class Admin(db.Model):
    __tablename__="admin"
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    admin_id=db.Column(db.String,unique=True, nullable=False)
    password=db.Column(db.String,nullable=False)
    active=db.Column(db.Boolean)

    
class Products(db.Model):
    __tablename__="products"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    category_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
    product_name=db.Column(db.String, nullable=False, unique=True)
    unit=db.Column(db.String,nullable=False)
    rate=db.Column(db.Float, nullable=False)
    quantity=db.Column(db.Float, nullable=False)
    image=db.Column(db.LargeBinary)    
    category=db.relationship('Category', backref='products', lazy=True)
    
class Category(db.Model):
    __tablename__="categories"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True)
    description=db.Column(db.String)
    image=db.Column(db.LargeBinary)
    
class Units(db.Model):
    __tablename__="units"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    name=db.Column(db.String, unique=True, nullable=False)

class Cart(db.Model):
    __tablename__="cart"
    cart_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
    quantity=db.Column(db.Float,nullable=False)
    total=db.Column(db.Float,nullable=False)
    user=db.relationship('User', backref='cart', lazy=True)
    product=db.relationship('Products', backref='cart', lazy=False)
    
class Orders(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_id=db.Column(db.Integer, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    category_name=db.Column(db.String,nullable=False)
    product_name=db.Column(db.String, nullable=False)
    quantity=db.Column(db.String,nullable=False)
    rate=db.Column(db.String, nullable=False)
    total=db.Column(db.Float,nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
