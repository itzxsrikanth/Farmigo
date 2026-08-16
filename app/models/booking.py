from datetime import datetime
from enum import Enum

from app.extensions import db


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default=BookingStatus.PENDING.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship("Payment", backref="booking", uselist=False)

    def __repr__(self):
        return f"<Booking #{self.id} eq={self.equipment_id} status={self.status}>"
