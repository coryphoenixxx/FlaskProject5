from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash


db = SQLAlchemy()
migrate = Migrate()


dishes_categories_association = db.Table('dishes_categories',
                                         db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id')),
                                         db.Column('categories_id', db.Integer, db.ForeignKey('categories.id'))
                                         )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order')

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    total = db.Column(db.REAL, nullable=False)
    status = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    addr = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    dishes = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.REAL, nullable=False)
    desc = db.Column(db.String, nullable=False)
    pic = db.Column(db.String, nullable=False)
    categories = db.relationship('Category', secondary=dishes_categories_association, back_populates='dishes')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    dishes = db.relationship('Dish', secondary=dishes_categories_association, back_populates='categories')
