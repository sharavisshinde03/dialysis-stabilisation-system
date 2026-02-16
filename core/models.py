from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TreatmentSession(db.Model):
    __tablename__ = "treatment_sessions"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))  # RUNNING / COMPLETED / EMERGENCY_STOP


class SystemEvent(db.Model):
    __tablename__ = "system_events"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("treatment_sessions.id"))
    event_type = db.Column(db.String(50))  # STABILISATION / EMERGENCY_STOP
    vibration_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
