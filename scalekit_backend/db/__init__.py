from flask_sqlalchemy import SQLAlchemy
# from scalekit_backend.db import models

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all() 