from flask import Blueprint, render_template, session, redirect, url_for, request
from models import PatientRequest, Prescription, User
from database import db

doctor_bp = Blueprint("doctor_routes", __name__)

# -------------------------
# Helper decorator: doctor login required
# -------------------------
def doctor_login_required(f):
    def wrapper(*args, **kwargs):
        if session.get("role") != "doctor":
            return redirect(url_for("auth_routes.login_page"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# -------------------------
# Doctor Dashboard
# -------------------------
@doctor_bp.route("/dashboard")
@doctor_login_required
def dashboard():
    return render_template("doctor_dashboard.html")

# -------------------------
# New Requests (Pending)
# -------------------------
@doctor_bp.route("/new_requests")
@doctor_login_required
def new_requests():
    requests = PatientRequest.query.filter_by(status="Pending").all()
    return render_template("doctor_new_requests.html", requests=requests)

# -------------------------
# Already Prescribed Requests
# -------------------------
@doctor_bp.route("/prescribed_requests")
@doctor_login_required
def prescribed_requests():
    prescriptions = Prescription.query.all()
    return render_template("doctor_prescribed.html", prescriptions=prescriptions)

# -------------------------
# Prescribe / Respond to Request
# -------------------------
@doctor_bp.route("/prescribe/<int:request_id>", methods=["GET", "POST"])
@doctor_login_required
def prescribe(request_id):
    patient_request = PatientRequest.query.get_or_404(request_id)

    if request.method == "POST":
        advice = request.form.get("advice")
        prescription = Prescription(
            request_id=patient_request.id,
            doctor_id=session["user_id"],
            advice=advice
        )
        # Update request status to Reviewed
        patient_request.status = "Reviewed"

        db.session.add(prescription)
        db.session.commit()

        return redirect(url_for("doctor_routes.prescribed_requests"))  # Go to Already Prescribed page

    return render_template("doctor_prescribe.html", request=patient_request)
