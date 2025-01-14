from flask import Blueprint, jsonify, request
from config import db
from models.user_model import User, user_schema, users_schema
# Removed: from authenticator import auth_required

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/", methods=["GET"])
def get_users():
    # Exclude passwords when retrieving all users
    users = User.query.with_entities(User.UserID, User.Name, User.Email_address, User.Role).all()
    return jsonify([
        {
            "UserID": user.UserID,
            "Name": user.Name,
            "Email_address": user.Email_address,
            "Role": user.Role
        } 
        for user in users
    ])

@users_blueprint.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    Retrieve user details by ID.
    """
    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # Exclude password from response
    user_data = {
        "UserID": user.UserID,
        "Name": user.Name,
        "Email_address": user.Email_address,
        "Role": user.Role
    }
    return jsonify(user_data), 200

@users_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    email = data.get("Email_address")

    # Check if email already exists
    existing_user = User.query.filter_by(Email_address=email).first()
    if existing_user:
        return jsonify({"error": "Email address already exists. Please log in or use a different email address."}), 400

    # Automatically set UserID as the next highest integer
    max_user_id = db.session.query(db.func.max(User.UserID)).scalar() or 0
    new_user = User(
        UserID=max_user_id + 1,
        Name=data.get("Name"),
        Email_address=email,
        Password=data.get("Password"),
        Role=data.get("Role")
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@users_blueprint.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update an existing user in the database.
    :param user_id: The ID of the user to be updated.
    :return: The updated user data or an error message.
    """
    data = request.get_json()

    # Find the user by UserID
    user = User.query.filter_by(UserID=user_id).first()

    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # Update the fields (except UserID)
    if "Name" in data:
        user.Name = data["Name"]
    if "Email_address" in data:
        # Ensure email uniqueness
        existing_user = User.query.filter_by(Email_address=data["Email_address"]).first()
        if existing_user and existing_user.UserID != user_id:
            return jsonify({"error": "Email address already in use"}), 400
        user.Email_address = data["Email_address"]
    if "Password" in data:
        user.Password = data["Password"]
    if "Role" in data:
        user.Role = data["Role"]

    # Commit the changes to the database
    db.session.commit()

    return user_schema.jsonify(user), 200

@users_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user from the database by ID.
    :param user_id: The ID of the user to delete.
    :return: Success message or error if user not found.
    """
    # Find the user by UserID
    user = User.query.filter_by(UserID=user_id).first()

    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User with ID {user_id} has been deleted successfully"}), 200
