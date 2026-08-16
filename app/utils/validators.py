import os
import uuid

from flask import current_app


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
    )


def save_equipment_image(file_storage) -> str | None:
    """Save an uploaded equipment image with a unique filename. Returns the stored filename."""
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename):
        raise ValueError("Unsupported file type.")

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    upload_path = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_path, exist_ok=True)
    file_storage.save(os.path.join(upload_path, unique_name))
    return unique_name
