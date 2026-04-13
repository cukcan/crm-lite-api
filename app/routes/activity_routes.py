from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Lead, Activity

activity_bp = Blueprint("activity_bp", __name__)


def get_owned_lead_or_404(lead_id: int, user_id: int):
    lead = Lead.query.filter_by(id=lead_id, owner_id=user_id).first()
    if not lead:
        return None
    return lead


@activity_bp.get("/lead/<int:lead_id>")
@jwt_required()
def get_activities_for_lead(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = get_owned_lead_or_404(lead_id, current_user_id)

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    activities = (
        Activity.query.filter_by(lead_id=lead.id)
        .order_by(Activity.created_at.desc())
        .all()
    )
    return jsonify([activity.to_dict() for activity in activities]), 200


@activity_bp.get("/<int:activity_id>")
@jwt_required()
def get_activity(activity_id: int):
    current_user_id = int(get_jwt_identity())

    activity = (
        Activity.query.join(Lead, Activity.lead_id == Lead.id)
        .filter(Activity.id == activity_id, Lead.owner_id == current_user_id)
        .first()
    )

    if not activity:
        return jsonify({"error": "Activity not found."}), 404

    return jsonify(activity.to_dict()), 200


@activity_bp.post("/lead/<int:lead_id>")
@jwt_required()
def create_activity(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = get_owned_lead_or_404(lead_id, current_user_id)

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    data = request.get_json(silent=True) or {}

    activity_type = data.get("type")
    description = data.get("description")
    due_date_str = data.get("due_date")
    completed = data.get("completed", False)

    if not activity_type or not str(activity_type).strip():
        return jsonify({"error": "Field 'type' is required."}), 400

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            return jsonify(
                {"error": "Field 'due_date' must be a valid ISO datetime string."}
            ), 400

    activity = Activity(
        lead_id=lead.id,
        type=str(activity_type).strip(),
        description=description.strip() if isinstance(description, str) else description,
        due_date=due_date,
        completed=bool(completed),
    )

    db.session.add(activity)
    db.session.commit()

    return jsonify(
        {
            "message": "Activity created successfully.",
            "activity": activity.to_dict(),
        }
    ), 201


@activity_bp.put("/<int:activity_id>")
@jwt_required()
def update_activity(activity_id: int):
    current_user_id = int(get_jwt_identity())

    activity = (
        Activity.query.join(Lead, Activity.lead_id == Lead.id)
        .filter(Activity.id == activity_id, Lead.owner_id == current_user_id)
        .first()
    )

    if not activity:
        return jsonify({"error": "Activity not found."}), 404

    data = request.get_json(silent=True) or {}

    if "type" in data:
        if not data["type"] or not str(data["type"]).strip():
            return jsonify({"error": "Field 'type' cannot be empty."}), 400
        activity.type = str(data["type"]).strip()

    if "description" in data:
        description = data["description"]
        activity.description = (
            description.strip() if isinstance(description, str) else description
        )

    if "due_date" in data:
        due_date_str = data["due_date"]
        if due_date_str:
            try:
                activity.due_date = datetime.fromisoformat(due_date_str)
            except ValueError:
                return jsonify(
                    {"error": "Field 'due_date' must be a valid ISO datetime string."}
                ), 400
        else:
            activity.due_date = None

    if "completed" in data:
        activity.completed = bool(data["completed"])

    db.session.commit()

    return jsonify(
        {
            "message": "Activity updated successfully.",
            "activity": activity.to_dict(),
        }
    ), 200


@activity_bp.delete("/<int:activity_id>")
@jwt_required()
def delete_activity(activity_id: int):
    current_user_id = int(get_jwt_identity())

    activity = (
        Activity.query.join(Lead, Activity.lead_id == Lead.id)
        .filter(Activity.id == activity_id, Lead.owner_id == current_user_id)
        .first()
    )

    if not activity:
        return jsonify({"error": "Activity not found."}), 404

    db.session.delete(activity)
    db.session.commit()

    return jsonify({"message": "Activity deleted successfully."}), 200