from extensions import db
from models import User
from werkzeug.security import generate_password_hash
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def migrate_passwords():
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.password and not user.password.startswith("pbkdf2:sha256"):
                user.password = generate_password_hash(user.password)
                db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
    migrate_passwords()
