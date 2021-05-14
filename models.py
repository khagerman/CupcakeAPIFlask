"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
GENERIC_IMAGE = "https://tinyurl.com/demo-cupcake"


class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcake"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    flavor = db.Column(
        db.Text,
        nullable=False,
    )
    size = db.Column(
        db.Text,
        nullable=False,
    )

    rating = db.Column(db.Float(), nullable=False)
    image = db.Column(db.Text, default=GENERIC_IMAGE)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
