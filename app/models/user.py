from sqlalchemy.orm import mapped_column

from app.db import db

class User(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    name = mapped_column(db.String(100), nullable=False)
    email = mapped_column(db.String(120), unique=True, nullable=False)
    lastname = mapped_column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
