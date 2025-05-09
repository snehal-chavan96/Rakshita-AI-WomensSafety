from flask_sqlalchemy import SQLAlchemy
from config import Config  # Import Config class

db = SQLAlchemy()

def init_db(app):
    app.config.from_object(Config)  # Load all configurations from Config class
    db.init_app(app)
    with app.app_context():
        db.create_all()
