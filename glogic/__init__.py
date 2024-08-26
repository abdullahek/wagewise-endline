from glogic.config import config_env_files
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

# initialises app and db
db = SQLAlchemy()
app = Flask(__name__)


# prepares the app and db environment based on config files
def prepare_app(environment='ms', p_db=db):
    app.config.from_object(config_env_files[environment])
    p_db.init_app(app)
    # load views by importing them
    from . import views
    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()


db.save = save_and_commit
