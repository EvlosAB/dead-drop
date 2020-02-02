import os

from datetime import datetime, timedelta
from flask import Flask
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

from .db import db
from .controllers import dd_blueprint
from .models import EncryptedInformation


def remove_old_encrypted_info():
    """
    Delete all rows older than 24 hours
    """
    with flask_app().app_context():
        twentyfourhours = datetime.now() - timedelta(hours=24)

        old_rows = EncryptedInformation.query.filter(
            EncryptedInformation.created_at > twentyfourhours
        ).all()

        for old_row in old_rows:
            db.session.delete(old_row)

        db.session.commit()


def flask_app(start_scheduler: bool = False):
    app = Flask(__name__)

    # Init database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://'
        f'{os.environ["DB_USER"]}'
        f':{os.environ["DB_PASSWORD"]}'
        f'@{os.environ["DB_HOST"]}'
        f':{os.environ["DB_PORT"]}'
        f'/{os.environ["DB_NAME"]}?charset=utf8mb4'
    )
    db.init_app(app)

    Migrate(app, db)

    app.register_blueprint(dd_blueprint)

    # Start scheduler to remove rows older than 24 hours
    if start_scheduler:
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(remove_old_encrypted_info, 'interval', minutes=10)

    return app
