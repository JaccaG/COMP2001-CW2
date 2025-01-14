from flask import Blueprint, jsonify
from config import db
from models.feature_model import Feature, feature_schema, features_schema
from models.trail_feature_model import TrailFeature, trail_feature_schema, trail_features_schema

# Blueprint for general Feature endpoints
features_blueprint = Blueprint("features_blueprint", __name__)
# Blueprint for linking Trail to Feature
trail_features_blueprint = Blueprint("trail_features_blueprint", __name__)

@features_blueprint.route("/", methods=["GET"])
def get_all_features():
    """
    Retreives all featres from the FEATURE table.
    """
    try:
        all_features = Feature.query.all()
        return features_schema.jsonify(all_features), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trail_features_blueprint.route("/", methods=["GET"])
def get_all_trail_features():
    """
    Retrives all records from the TRAIL_FEATURE table (which link Trails to Featues).
    """
    try:
        all_trail_features = TrailFeature.query.all()
        return trail_features_schema.jsonify(all_trail_features), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
