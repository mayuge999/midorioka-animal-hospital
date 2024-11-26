from datetime import datetime, time
from flask_login import UserMixin
from app import db, JST

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)
    max_slots = db.Column(db.Integer, default=3)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, time_str, max_slots=3):
        self.time = datetime.strptime(time_str, '%H:%M').time()
        self.max_slots = max_slots

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_owner = db.Column(db.String(100), nullable=False)
    pet_name = db.Column(db.String(100), nullable=False)
    pet_type = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(JST))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread', index=True)  # unread, read, replied
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
