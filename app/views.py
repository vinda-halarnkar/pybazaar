from flask import Blueprint, render_template

from app.db import db
from app.models.user import User

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # user = db.session.execute(db.select(User)).scalar()
    # print(user)
    return render_template("index.html")