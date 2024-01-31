import os
from flask import Flask
from views import views

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SECURITY_REGISTERABLE'] = True
    app.register_blueprint(views, url_prefix="/")
    return app 


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5050)