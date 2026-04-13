from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not email:
        return jsonify({"error": "Field 'email' is required."}), 400

    if not password:
        return jsonify({"error": "Field 'password' is required."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    existing_user = User.query.filter_by(email=email.strip().lower()).first()
    if existing_user:
        return jsonify({"error": "A user with this email already exists."}), 409

    user = User(
        full_name=full_name.strip() if full_name else None,
        email=email.strip().lower(),
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "message": "User registered successfully.",
            "user": user.to_dict(),
        }
    ), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email:
        return jsonify({"error": "Field 'email' is required."}), 400

    if not password:
        return jsonify({"error": "Field 'password' is required."}), 400

    user = User.query.filter_by(email=email.strip().lower()).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    if not user.is_active:
        return jsonify({"error": "User account is inactive."}), 403

    access_token = create_access_token(identity=str(user.id))

    return jsonify(
        {
            "message": "Login successful.",
            "access_token": access_token,
            "user": user.to_dict(),
        }
    ), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)

    return jsonify({"user": user.to_dict()}), 200