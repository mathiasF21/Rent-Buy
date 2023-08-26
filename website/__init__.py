import secrets
from flask import Flask, render_template
from flask_login import LoginManager
from .database import Database

db = Database()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_urlsafe(32)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    init_app(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .user_views import bp as users_bp
    app.register_blueprint(users_bp)

    from .home import bp as home_bp
    app.register_blueprint(home_bp)

    from .sign_in import bp as sign_bp
    app.register_blueprint(sign_bp)

    from .car_info_views import bp as car_bp
    app.register_blueprint(car_bp)

    from .cars_api import bp as cars_api_bp
    app.register_blueprint(cars_api_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.logout'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_user_id(int(user_id))

    return app

def init_app(app):
    app.teardown_appcontext(cleanup)

def cleanup(value):
    pass
