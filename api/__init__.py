from flask import Flask
from .routes.home import home
from .routes.league_id import league_id_blueprint

def createapp(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    app.register_blueprint(home)
    app.register_blueprint(league_id_blueprint)

    return app