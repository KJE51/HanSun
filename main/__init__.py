from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트
    from .views import main_views, payment_views, function_views, user_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(function_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(payment_views.bp)

    return app