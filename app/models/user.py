from datetime import datetime
from enum import Enum

from flask_login import UserMixin

from app.extensions import db, bcrypt


class UserRole(str, Enum):
    FARMER = "farmer"
    OWNER = "owner"
    ADMIN = "admin"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default=UserRole.FARMER.value, nullable=False)
    village = db.Column(db.String(120), nullable=True)
    district = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    equipment_listings = db.relationship(
        "Equipment", backref="owner", lazy=True, foreign_keys="Equipment.owner_id"
    )
    bookings = db.relationship(
        "Booking", backref="renter", lazy=True, foreign_keys="Booking.renter_id"
    )
    reviews = db.relationship("Review", backref="author", lazy=True)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    def is_owner(self) -> bool:
        return self.role == UserRole.OWNER.value

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN.value

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
