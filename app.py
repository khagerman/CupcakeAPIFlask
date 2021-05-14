"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcake_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON  of all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:id>")
def list_single_cupcake(id):
    """Get data about a single cupcake."""

    cupcake = Cupcake.query.get(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake from form data & return it."""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)
    # end create_cupcake


@app.route("/")
def home():
    """Render homepage."""

    return render_template("index.html")


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)

    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.image = request.json.get("image", cupcake.image)
    serialized = serialize_cupcake(cupcake)
    db.session.commit()
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
