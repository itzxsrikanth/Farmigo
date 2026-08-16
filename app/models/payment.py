from datetime import datetime
from enum import Enum

from app.extensions import db


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(30), default="mock_gateway")
    transaction_ref = db.Column(db.String(100), unique=True, nullable=True)
    status = db.Column(db.String(20), default=PaymentStatus.PENDING.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment #{self.id} status={self.status}>"
