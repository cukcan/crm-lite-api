from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Lead, Company, PipelineStage

lead_bp = Blueprint("lead_bp", __name__)


@lead_bp.get("/")
@jwt_required()
def get_leads():
    current_user_id = int(get_jwt_identity())
    leads = Lead.query.filter_by(owner_id=current_user_id).order_by(Lead.id.asc()).all()
    return jsonify([lead.to_dict() for lead in leads]), 200


@lead_bp.get("/<int:lead_id>")
@jwt_required()
def get_lead(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = Lead.query.filter_by(id=lead_id, owner_id=current_user_id).first()

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    return jsonify(lead.to_dict()), 200


@lead_bp.post("/")
@jwt_required()
def create_lead():
    current_user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not first_name:
        return jsonify({"error": "Field 'first_name' is required."}), 400
    if not last_name:
        return jsonify({"error": "Field 'last_name' is required."}), 400

    if email:
        existing_email = Lead.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({"error": "A lead with this email already exists."}), 409

    company_id = data.get("company_id")
    if company_id is not None:
        company = Company.query.get(company_id)
        if not company:
            return jsonify({"error": "Invalid company_id."}), 400

    stage_id = data.get("stage_id")
    if stage_id is not None:
        stage = PipelineStage.query.get(stage_id)
        if not stage:
            return jsonify({"error": "Invalid stage_id."}), 400

    lead = Lead(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email,
        phone=data.get("phone"),
        source=data.get("source"),
        status=data.get("status", "open"),
        company_id=company_id,
        stage_id=stage_id,
        owner_id=current_user_id,
    )

    db.session.add(lead)
    db.session.commit()

    return jsonify(
        {
            "message": "Lead created successfully.",
            "lead": lead.to_dict(),
        }
    ), 201


@lead_bp.put("/<int:lead_id>")
@jwt_required()
def update_lead(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = Lead.query.filter_by(id=lead_id, owner_id=current_user_id).first()

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    data = request.get_json(silent=True) or {}

    if "first_name" in data:
        if not data["first_name"]:
            return jsonify({"error": "Field 'first_name' cannot be empty."}), 400
        lead.first_name = data["first_name"].strip()

    if "last_name" in data:
        if not data["last_name"]:
            return jsonify({"error": "Field 'last_name' cannot be empty."}), 400
        lead.last_name = data["last_name"].strip()

    if "email" in data:
        new_email = data["email"]
        if new_email:
            existing_email = Lead.query.filter(
                Lead.email == new_email,
                Lead.id != lead.id,
            ).first()
            if existing_email:
                return jsonify({"error": "Another lead already uses this email."}), 409
        lead.email = new_email

    if "phone" in data:
        lead.phone = data["phone"]

    if "source" in data:
        lead.source = data["source"]

    if "status" in data:
        lead.status = data["status"]

    if "company_id" in data:
        company_id = data["company_id"]
        if company_id is not None:
            company = Company.query.get(company_id)
            if not company:
                return jsonify({"error": "Invalid company_id."}), 400
        lead.company_id = company_id

    if "stage_id" in data:
        stage_id = data["stage_id"]
        if stage_id is not None:
            stage = PipelineStage.query.get(stage_id)
            if not stage:
                return jsonify({"error": "Invalid stage_id."}), 400
        lead.stage_id = stage_id

    db.session.commit()

    return jsonify(
        {
            "message": "Lead updated successfully.",
            "lead": lead.to_dict(),
        }
    ), 200


@lead_bp.delete("/<int:lead_id>")
@jwt_required()
def delete_lead(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = Lead.query.filter_by(id=lead_id, owner_id=current_user_id).first()

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    db.session.delete(lead)
    db.session.commit()

    return jsonify({"message": "Lead deleted successfully."}), 200