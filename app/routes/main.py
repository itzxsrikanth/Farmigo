import json
from collections import Counter
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import Booking, Equipment, EquipmentCategory

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    featured = Equipment.query.filter_by(is_available=True).order_by(
        Equipment.created_at.desc()
    ).limit(6).all()
    return render_template("index.html", featured=featured)


def _get_map_data(equipment_list):
    # Location coordinates mapping for 13+ major agricultural hubs across India
    coords = {
        "ludhiana": (30.9010, 75.8573),
        "punjab": (30.9010, 75.8573),
        "karnal": (29.6857, 76.9905),
        "haryana": (29.6857, 76.9905),
        "nashik": (19.9975, 73.7898),
        "maharashtra": (19.9975, 73.7898),
        "bareilly": (28.3670, 79.4304),
        "up": (28.3670, 79.4304),
        "pradesh": (28.3670, 79.4304),
        "guntur": (16.3067, 80.4365),
        "andhra": (16.3067, 80.4365),
        "anand": (22.5645, 72.9289),
        "gujarat": (22.5645, 72.9289),
        "mandya": (12.5218, 76.8951),
        "karnataka": (12.5218, 76.8951),
        "pollachi": (10.6609, 77.0048),
        "tamil": (10.6609, 77.0048),
        "nadu": (10.6609, 77.0048),
        "indore": (22.7196, 75.8577),
        "madhya": (22.7196, 75.8577),
        "bhubaneswar": (20.2961, 85.8245),
        "odisha": (20.2961, 85.8245),
        "bikaner": (28.0229, 73.3119),
        "rajasthan": (28.0229, 73.3119),
        "patna": (25.5941, 85.1376),
        "bihar": (25.5941, 85.1376),
        "bardhaman": (23.2324, 87.8615),
        "bengal": (23.2324, 87.8615),
        "west bengal": (23.2324, 87.8615),
        "coimbatore": (11.0168, 76.9558),
        "erode": (11.3410, 77.7172),
        "salem": (11.6643, 78.1460),
        "tiruppur": (11.1085, 77.3411),
    }

    map_data = []
    for idx, item in enumerate(equipment_list):
        loc_key = item.location.lower()
        lat, lng = 20.5937 + ((idx - 5) * 1.2), 78.9629 + ((idx - 5) * 1.1)
        for key in coords:
            if key in loc_key:
                lat, lng = coords[key]
                # slight offset to avoid exact marker overlap
                lat += (idx * 0.005)
                lng += (idx * 0.005)
                break

        map_data.append({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price_per_day": float(item.price_per_day),
            "location": item.location,
            "brand": item.brand or "Generic",
            "image_filename": item.image_filename or "",
            "lat": lat,
            "lng": lng
        })
    return json.dumps(map_data)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    all_available = Equipment.query.filter_by(is_available=True).all()
    map_json = _get_map_data(all_available)

    if current_user.is_owner():
        listings = Equipment.query.filter_by(owner_id=current_user.id).all()
        incoming = (
            Booking.query.join(Equipment)
            .filter(Equipment.owner_id == current_user.id)
            .order_by(Booking.created_at.desc())
            .all()
        )
        
        # Calculate Owner Analytics
        total_earnings = sum(float(b.total_amount) for b in incoming)
        active_count = sum(1 for e in listings if e.is_available)
        
        # Category breakdown for owner listings
        cat_counts = Counter(e.category for e in listings)
        all_cats = [c.value for c in EquipmentCategory]
        category_data = [cat_counts.get(c, 0) for c in all_cats]
        
        # Monthly Revenue Trend (sample distribution for demo visualization)
        months = ["Mar", "Apr", "May", "Jun", "Jul", "Aug"]
        monthly_revenue = [
            round(total_earnings * 0.1, 0),
            round(total_earnings * 0.15, 0),
            round(total_earnings * 0.2, 0),
            round(total_earnings * 0.18, 0),
            round(total_earnings * 0.22, 0),
            round(total_earnings * 0.15, 0),
        ] if total_earnings > 0 else [1200, 2400, 3600, 4800, 6000, 7200]

        return render_template(
            "dashboard/owner.html",
            listings=listings,
            bookings=incoming[:10],
            total_earnings=total_earnings,
            active_count=active_count,
            total_bookings=len(incoming),
            cat_labels=json.dumps([c.capitalize() for c in all_cats]),
            cat_data=json.dumps(category_data),
            months=json.dumps(months),
            monthly_revenue=json.dumps(monthly_revenue),
            map_data=map_json
        )

    if current_user.is_admin():
        total_users = Equipment.query.count()
        return render_template("dashboard/admin.html", total_equipment=total_users)

    # Farmer Dashboard Logic
    my_bookings = (
        Booking.query.filter_by(renter_id=current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    
    total_spent = sum(float(b.total_amount) for b in my_bookings)
    total_days = sum(b.total_days for b in my_bookings)
    
    # Category usage breakdown for farmer
    cat_counts = Counter(b.equipment.category for b in my_bookings if b.equipment)
    all_cats = [c.value for c in EquipmentCategory]
    category_data = [cat_counts.get(c, 0) for c in all_cats]

    months = ["Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    monthly_spent = [
        round(total_spent * 0.12, 0),
        round(total_spent * 0.18, 0),
        round(total_spent * 0.25, 0),
        round(total_spent * 0.15, 0),
        round(total_spent * 0.20, 0),
        round(total_spent * 0.10, 0),
    ] if total_spent > 0 else [600, 1200, 1800, 2400, 3000, 3600]

    return render_template(
        "dashboard/farmer.html",
        bookings=my_bookings[:10],
        total_spent=total_spent,
        total_days=total_days,
        total_bookings=len(my_bookings),
        cat_labels=json.dumps([c.capitalize() for c in all_cats]),
        cat_data=json.dumps(category_data),
        months=json.dumps(months),
        monthly_spent=json.dumps(monthly_spent),
        map_data=map_json
    )
