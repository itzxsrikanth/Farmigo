"""Populate the database with 13+ demo machinery items across 13 states in India.
Run with: python seed.py
"""
from app import create_app
from app.extensions import db
from app.models import User, Equipment, UserRole, EquipmentCategory

app = create_app("development")

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="owner@example.com").first():
        owner = User(full_name="Ramesh Kumar", email="owner@example.com",
                     role=UserRole.OWNER.value, village="Pollachi", district="Coimbatore")
        owner.set_password("password123")
        db.session.add(owner)

    if not User.query.filter_by(email="farmer@example.com").first():
        farmer = User(full_name="Suresh Nair", email="farmer@example.com",
                      role=UserRole.FARMER.value, village="Mettupalayam", district="Coimbatore")
        farmer.set_password("password123")
        db.session.add(farmer)

    db.session.commit()
    owner = User.query.filter_by(email="owner@example.com").first()

    demo_items = [
        ("Mahindra 575 DI Tractor", EquipmentCategory.TRACTOR.value, "Mahindra", 1200, "Pollachi, Tamil Nadu", "tractor_mahindra.png"),
        ("John Deere Combine Harvester", EquipmentCategory.HARVESTER.value, "John Deere", 3500, "Ludhiana, Punjab", "combine_harvester.png"),
        ("Sonalika Heavy Duty 750 DI", EquipmentCategory.TRACTOR.value, "Sonalika", 1400, "Karnal, Haryana", "tractor_mahindra.png"),
        ("Kubota Vineyard Mini Tractor", EquipmentCategory.TRACTOR.value, "Kubota", 1100, "Nashik, Maharashtra", "power_tiller.png"),
        ("Power Tiller 7HP", EquipmentCategory.TILLER.value, "VST Shakti", 600, "Mandya, Karnataka", "power_tiller.png"),
        ("Reversible MB Plough", EquipmentCategory.PLOUGH.value, "Lemken", 400, "Bareilly, Uttar Pradesh", "reversible_plough.png"),
        ("Boom Sprayer 400L", EquipmentCategory.SPRAYER.value, "Aspee", 800, "Anand, Gujarat", "boom_sprayer.png"),
        ("Agri Drone Sprayer", EquipmentCategory.DRONE.value, "Garuda", 2500, "Guntur, Andhra Pradesh", "agri_drone.png"),
        ("Preet Heavy Duty 9049 Tractor", EquipmentCategory.TRACTOR.value, "Preet", 1600, "Indore, Madhya Pradesh", "tractor_mahindra.png"),
        ("Kubota Automatic Paddy Transplanter", EquipmentCategory.HARVESTER.value, "Kubota", 1800, "Bhubaneswar, Odisha", "combine_harvester.png"),
        ("Heavy Duty Rotary Tiller", EquipmentCategory.TILLER.value, "Shrachi", 750, "Bikaner, Rajasthan", "power_tiller.png"),
        ("Multicrop High-Speed Thresher", EquipmentCategory.HARVESTER.value, "Kirloskar", 1300, "Patna, Bihar", "combine_harvester.png"),
        ("Solar Crop Harvester Unit", EquipmentCategory.HARVESTER.value, "FieldKing", 2200, "Bardhaman, West Bengal", "combine_harvester.png"),
    ]
    for name, cat, brand, price, loc, img in demo_items:
        item = Equipment.query.filter_by(name=name).first()
        if not item:
            db.session.add(Equipment(
                owner_id=owner.id, name=name, category=cat, brand=brand,
                description=f"Well-maintained {name.lower()} available for daily rental.",
                price_per_day=price, location=loc, image_filename=img
            ))
        else:
            item.location = loc
            item.image_filename = img
            db.session.add(item)
    db.session.commit()
    print("13+ Location Seeding Complete! Login as owner@example.com / farmer@example.com, password: password123")
