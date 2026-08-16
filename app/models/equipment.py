from datetime import datetime
from enum import Enum

from app.extensions import db


class EquipmentCategory(str, Enum):
    TRACTOR = "tractor"
    HARVESTER = "harvester"
    TILLER = "tiller"
    PLOUGH = "plough"
    SPRAYER = "sprayer"
    DRONE = "drone"
    IRRIGATION = "irrigation"
    OTHER = "other"


class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)
    brand = db.Column(db.String(80), nullable=True)
    price_per_day = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="equipment", lazy=True)
    reviews = db.relationship("Review", backref="equipment", lazy=True)

    def average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    def __repr__(self):
        return f"<Equipment {self.name} ({self.category})>"
