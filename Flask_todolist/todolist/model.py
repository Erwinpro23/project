from flask_login import UserMixin
from sqlalchemy.sql import func
from todolist import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_name = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    is_done = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.String(50), default="Processing")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))

    # Quan hệ: 1 User có nhiều Note
    notes = db.relationship("Note", backref="user", lazy=True)

    # ✅ Đặt __init__ ĐÚNG CHỖ
    def __init__(self, email, password, user_name):
        self.email = email
        self.password = password
        self.user_name = user_name

