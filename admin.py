from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import User, Category, Order, Dish


admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Dish, db.session))
