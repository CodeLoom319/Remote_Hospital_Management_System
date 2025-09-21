from flask import Flask
from database import db
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from models import User  # needed for seeding
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(patient_bp, url_prefix="/patient")
app.register_blueprint(doctor_bp, url_prefix="/doctor")


# Ensure new columns exist in the user table
def ensure_user_columns():
    columns_to_add = [
        ("name", "TEXT"),
        ("email", "TEXT"),
        ("phone", "TEXT")
    ]
    
    for col, col_type in columns_to_add:
        try:
            db.session.execute(text(f"ALTER TABLE user ADD COLUMN {col} {col_type}"))
            print(f"Added column {col} to user table")
        except Exception as e:
            # Column probably already exists, ignore
            pass
    db.session.commit()


# Seed doctors (only run if not already in DB)
def seed_doctors():
    doctors = [
        {"username": "dr_smith", "password": "1234"},
        {"username": "dr_john", "password": "1234"}
    ]
    
    for doc in doctors:
        exists = User.query.filter_by(username=doc["username"]).first()
        if not exists:
            new_doc = User(
                username=doc["username"],
                password=doc["password"],
                role="doctor",
                name=None,
                email=None,
                phone=None
            )
            db.session.add(new_doc)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()         # create tables if they don't exist
        ensure_user_columns()   # make sure name, email, phone exist
        seed_doctors()          # adds the doctors if not already present
    app.run(debug=True)
