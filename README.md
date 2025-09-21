# Remote Hospital Management System

A simple web-based remote hospital management system built with Flask and SQLite.  
This system allows patients to register, submit health requests, and view request history, while doctors can view new requests, prescribe advice, and track prescribed requests.

---

## Features

### For Patients
- Register and login
- Submit health requests with optional medical reports
- View request history and status

### For Doctors
- View new patient requests
- Prescribe advice
- Track already prescribed requests

---

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS (MDB UI Kit, Bootstrap, Bootstrap Icons)
- **Others:** JavaScript (for form submissions)

---

## Project Structure

project/
|
|-- app.py               
|-- models.py             
|-- database.py          
|-- routes/
|   |-- auth_routes.py    
|   |-- patient_routes.py
|   |-- doctor_routes.py
|-- templates/
|   |-- login.html
|   |-- register.html
|   |-- patient_dashboard.html
|   |-- doctor_dashboard.html
|   |-- new_request.html
|   |-- requests_history.html
|   |-- new_requests.html
|   |-- prescribed_requests.html
|   |-- prescribe.html
|-- static/               
|-- uploads/              


---

## Installation

1. **Clone the repository:**

git clone https://github.com/CodeLoom319/Remote_Hospital_Management_System.git
cd RemoteHospitalManagementSystem

2. Install dependencies:
pip install flask flask_sqlalchemy

3. Run the application:
python app.py

4. Access the app:
Open your browser and go to http://127.0.0.1:5000/auth/login
