from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Equipment, EquipmentCategory
from app.utils.decorators import role_required
from app.utils.validators import save_equipment_image

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@equipment_bp.route("/")
def list_equipment():
    category = request.args.get("category")
    location = request.args.get("location", "").strip()

    query = Equipment.query.filter_by(is_available=True)
    if category:
        query = query.filter_by(category=category)
    if location:
        query = query.filter(Equipment.location.ilike(f"%{location}%"))

    items = query.order_by(Equipment.created_at.desc()).all()
    categories = [c.value for c in EquipmentCategory]
    return render_template(
        "equipment/list.html", items=items, categories=categories,
        selected_category=category, location=location,
    )


@equipment_bp.route("/<int:equipment_id>")
def detail(equipment_id):
    item = Equipment.query.get_or_404(equipment_id)
    return render_template("equipment/detail.html", item=item, today=date.today())


@equipment_bp.route("/new", methods=["GET", "POST"])
@login_required
@role_required("owner", "admin")
def create():
    categories = [c.value for c in EquipmentCategory]

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category")
        description = request.form.get("description", "").strip()
        brand = request.form.get("brand", "").strip()
        price_per_day = request.form.get("price_per_day")
        location = request.form.get("location", "").strip()
        image_file = request.files.get("image")

        if not name or not category or not price_per_day or not location:
            flash("Please fill in all required fields.", "danger")
            return render_template("equipment/form.html", categories=categories, form_data=request.form)

        try:
            image_filename = save_equipment_image(image_file)
        except ValueError as exc:
            flash(str(exc), "danger")
            return render_template("equipment/form.html", categories=categories, form_data=request.form)

        item = Equipment(
            owner_id=current_user.id,
            name=name,
            category=category,
            description=description,
            brand=brand,
            price_per_day=price_per_day,
            location=location,
            image_filename=image_filename,
        )
        db.session.add(item)
        db.session.commit()
        flash("Equipment listed successfully.", "success")
        return redirect(url_for("equipment.detail", equipment_id=item.id))

    return render_template("equipment/form.html", categories=categories, form_data={})
