from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from models import User
from database import db

auth_bp = Blueprint("auth_routes", __name__)

# -------------------------
# Page Routes (HTML)
# -------------------------

# Root -> redirect to login
@auth_bp.route("/")
def root_redirect():
    return redirect(url_for("auth_routes.login_page"))

# Register page
@auth_bp.route("/register_page", methods=["GET"])
def register_page():
    return render_template("register.html")

# Login page (default for /login)
@auth_bp.route("/login_page", methods=["GET"])
@auth_bp.route("/login", methods=["GET"])  # <--- added so /login works
def login_page():
    return render_template("login.html")

# -------------------------
# Logout route
# -------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth_routes.login_page"))

# -------------------------
# API Routes (JSON + form)
# -------------------------

# Patient registration
@auth_bp.route("/register", methods=["POST"])
def register():
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
    
    # Check username and email uniqueness
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400
    
    new_user = User(
        username=username,
        password=password,
        role="patient",
        name=name,
        email=email,
        phone=phone
    )
    db.session.add(new_user)
    db.session.commit()
    
    if not request.is_json:
        return redirect(url_for("auth_routes.login_page"))
    
    return jsonify({"message": "Patient registered successfully!"})



# Login for patient & doctor
@auth_bp.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
    
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    
    session["user_id"] = user.id
    session["role"] = user.role

    # For frontend HTML redirect
    if not request.is_json:
        if user.role == "patient":
            return redirect("/patient/dashboard")
        else:
            return redirect("/doctor/dashboard")

    return jsonify({"message": f"Logged in as {user.role}"})
