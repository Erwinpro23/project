from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_login import LoginManager  # ✅ Sửa import ở đây

# --- Khởi tạo db ---
db = SQLAlchemy()
login_manager = LoginManager()  # ✅ Thêm dòng này

def create_app():
    load_dotenv()
    secret_key = os.getenv("Secret_Key")
    db_name = os.getenv("DB_Name")

    app = Flask(__name__)
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}.db"

    db.init_app(app)

    # Import model SAU khi init_app để tránh circular import
    from todolist.model import User, Note

    # Import và đăng ký blueprint
    from todolist.user import user
    from todolist.view import view
    app.register_blueprint(user)
    app.register_blueprint(view)

    # Tạo database nếu chưa có
    create_database(app, db_name)

    # ✅ Cấu hình Flask-Login
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    # ✅ Sửa cú pháp user_loader (không có dấu ngoặc)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app, db_name):
    db_path = f"todolist/{db_name}.db"
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("✅ Database Created")
    else:
        print("ℹ️ Database Already Exists")
