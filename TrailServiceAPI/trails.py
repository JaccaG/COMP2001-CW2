from flask import Blueprint, jsonify, request
from models.trail_model import Trail, trail_schema, trails_schema
from config import db

# Defines a blueprint for trail-related endpoints
trails_blueprint = Blueprint("trails_blueprint", __name__)

@trails_blueprint.route("/", methods=["GET"])
def get_trails():
    """
    Retrieves all trails.
    """
    try:
        trails = Trail.query.all()
        return trails_schema.jsonify(trails), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trails_blueprint.route("/trails/<int:trail_id>", methods=["GET"])
def get_trail(trail_id):
    """
    Retrieves a single trail by its ID.
    """
    try:
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"message": "Trail not found"}), 404
        return trail_schema.jsonify(trail), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trails_blueprint.route("/trails", methods=["POST"])
def create_trail():
    """
    Creates a new trail record.
    """
    try:
        data = request.get_json()
        required_fields = [
            "TrailName", "TrailSummary", "TrailDescription",
            "Difficulty", "Location", "Length", "ElevationGain", "RouteType"
        ]
        # Checks if all required fields are present in the data
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

        # Generates a new TrailID based on the current maximum
        max_trail_id = db.session.query(db.func.max(Trail.TrailID)).scalar() or 0
        new_trail = Trail(
            TrailID=max_trail_id + 1,
            TrailName=data.get("TrailName"),
            TrailSummary=data.get("TrailSummary"),
            TrailDescription=data.get("TrailDescription"),
            Difficulty=data.get("Difficulty"),
            Location=data.get("Location"),
            Length=data.get("Length"),
            ElevationGain=data.get("ElevationGain"),
            RouteType=data.get("RouteType"),
            OwnerID=None
        )

        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.jsonify(new_trail), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trails_blueprint.route("/trails/<int:trail_id>", methods=["PUT"])
def update_trail(trail_id):
    """
    Updates an existing trail.
    """
    try:
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"message": "Trail not found"}), 404

        data = request.get_json()
        # Defines which fields can be updated
        updatable_fields = [
            "TrailName", "TrailSummary", "TrailDescription",
            "Difficulty", "Location", "Length", "ElevationGain",
            "RouteType", "Pt1_Lat", "Pt1_Long", "Pt1_Desc",
            "Pt2_Lat", "Pt2_Long", "Pt2_Desc"
        ]

        # Updates only the allowed fields in the trail record
        for key, value in data.items():
            if key in updatable_fields:
                setattr(trail, key, value)

        db.session.commit()
        return trail_schema.jsonify(trail), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trails_blueprint.route("/trails/<int:trail_id>", methods=["DELETE"])
def delete_trail(trail_id):
    """
    Deletes a trail by its ID.
    """
    try:
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"message": "Trail not found"}), 404

        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
