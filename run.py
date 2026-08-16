import os

from app import create_app
from app.extensions import db

app = create_app(os.environ.get("FLASK_ENV", "development"))


@app.shell_context_processor
def make_shell_context():
    from app.models import User, Equipment, Booking, Payment, Review

    return {
        "db": db, "User": User, "Equipment": Equipment,
        "Booking": Booking, "Payment": Payment, "Review": Review,
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
