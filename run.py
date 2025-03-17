from dotenv import load_dotenv
from app import create_app
from app.models.user import User
from config import Config
from app.db import db  # Import db instance

load_dotenv()

app = create_app()
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

db.init_app(app)  # Initialize SQLAlchemy with Flask app

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=app.config['PORT'])

