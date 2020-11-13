import random

from flask import Flask

from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db, migrate


def shuffle(seq):
    random.shuffle(seq)
    return seq


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate.init_app(app, db)
csrf = CSRFProtect(app)
app.jinja_env.filters['shuffle'] = shuffle


from views import *
import admin


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
