from flask import Flask
from app.views import views

def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    # Register Blueprints
    app.register_blueprint(views)

    return app