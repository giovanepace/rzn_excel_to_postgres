from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.cache import cache
from app.views import blueprint
from app.database.db_init import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    cache.init_app(app)

    app.config.from_object('app.config.Config')

    db.init_app(app)

    app.register_blueprint(blueprint)

    with app.app_context():
        # Imports
        from . import views
        # Creates a table for our model
        db.create_all()
        return app


app = create_app()
