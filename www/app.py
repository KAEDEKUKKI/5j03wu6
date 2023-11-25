from flask import Flask
from config import Config
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    from auth.models import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.get_by_id(user_id)

    from main import main_bp
    app.register_blueprint(main_bp)

    from auth import auth_bp
    app.register_blueprint(auth_bp)

    from groups import group_bp
    app.register_blueprint(group_bp)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])