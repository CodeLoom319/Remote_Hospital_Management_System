from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "patient" or "doctor"

    # New fields for patient
    name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    # Optional: backrefs for convenience
    patient_requests = db.relationship("PatientRequest", backref="patient", lazy=True)
    prescriptions = db.relationship("Prescription", backref="doctor", lazy=True, foreign_keys="Prescription.doctor_id")


class PatientRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    report_file = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default="Pending")  # Pending / Reviewed

    # Relationship to prescriptions
    prescriptions = db.relationship("Prescription", backref="request", lazy=True)


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("patient_request.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    advice = db.Column(db.Text, nullable=False)

    # Relationships already covered with backrefs above
    # prescription.request → PatientRequest
    # prescription.doctor → User (doctor)
