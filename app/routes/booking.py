import uuid
from datetime import date, datetime

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Booking, Equipment, Payment, PaymentStatus

booking_bp = Blueprint("booking", __name__, url_prefix="/booking")


@booking_bp.route("/<int:equipment_id>/book", methods=["POST"])
@login_required
def create_booking(equipment_id):
    item = Equipment.query.get_or_404(equipment_id)

    try:
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        flash("Please choose valid start and end dates.", "danger")
        return redirect(url_for("equipment.detail", equipment_id=equipment_id))

    if start_date < date.today():
        flash("Booking start date cannot be in the past.", "danger")
        return redirect(url_for("equipment.detail", equipment_id=equipment_id))

    total_days = (end_date - start_date).days + 1
    if total_days < 1:
        flash("End date must be after the start date.", "danger")
        return redirect(url_for("equipment.detail", equipment_id=equipment_id))

    total_amount = total_days * float(item.price_per_day)

    booking = Booking(
        equipment_id=item.id,
        renter_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        total_days=total_days,
        total_amount=total_amount,
        status="pending",
    )
    db.session.add(booking)
    db.session.commit()

    # Mock payment gateway call — swap with Razorpay/Stripe order creation here.
    payment = Payment(
        booking_id=booking.id,
        amount=total_amount,
        method="mock_gateway",
        transaction_ref=f"TXN-{uuid.uuid4().hex[:10].upper()}",
        status=PaymentStatus.SUCCESS.value,
    )
    booking.status = "confirmed"
    db.session.add(payment)
    db.session.commit()

    flash(f"Booking confirmed! Reference: {payment.transaction_ref}", "success")
    return redirect(url_for("main.dashboard"))
