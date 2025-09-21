from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models import PatientRequest, Prescription, User
import os
from werkzeug.utils import secure_filename
from datetime import datetime

patient_bp = Blueprint("patient", __name__, template_folder="../templates")

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------
# Dashboard
# -------------------------
@patient_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("auth_routes.login_page"))

    patient_id = session["user_id"]

    total_requests = PatientRequest.query.filter_by(patient_id=patient_id).count()
    responded = PatientRequest.query.filter_by(patient_id=patient_id, status="Reviewed").count()
    pending = PatientRequest.query.filter_by(patient_id=patient_id, status="Pending").count()

    return render_template("patient_dashboard.html",
                           total_requests=total_requests,
                           responded=responded,
                           pending=pending)

# -------------------------
# New Request
# -------------------------
@patient_bp.route("/new_request", methods=["GET", "POST"])
def new_request():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("auth_routes.login_page"))

    if request.method == "POST":
        symptoms = request.form.get("symptoms")
        report_file = None

        if "report" in request.files:
            file = request.files["report"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                report_file = filename

        new_req = PatientRequest(patient_id=session["user_id"], symptoms=symptoms, report_file=report_file)
        db.session.add(new_req)
        db.session.commit()
        flash("Request submitted successfully!")
        return redirect(url_for("patient.dashboard"))

    return render_template("new_request.html")

# -------------------------
# Request History
# -------------------------
@patient_bp.route("/requests")
def requests_list():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("auth_routes.login_page"))

    patient_id = session["user_id"]
    requests = PatientRequest.query.filter_by(patient_id=patient_id).all()

    history = []
    for req in requests:
        prescription = Prescription.query.filter_by(request_id=req.id).first()
        history.append({
            "id": req.id,
            "symptoms": req.symptoms,
            "date": req.id,  # replace with timestamp if added
            "status": req.status,
            "report_file": req.report_file,
            "prescription": prescription.advice if prescription else None
        })

    return render_template("requests_history.html", history=history)
