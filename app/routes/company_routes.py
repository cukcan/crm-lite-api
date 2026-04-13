from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Company

company_bp = Blueprint("company_bp", __name__)


@company_bp.get("/")
@jwt_required()
def get_companies():
    companies = Company.query.order_by(Company.id.asc()).all()
    return jsonify([company.to_dict() for company in companies]), 200


@company_bp.get("/<int:company_id>")
@jwt_required()
def get_company(company_id: int):
    company = Company.query.get_or_404(company_id)
    return jsonify(company.to_dict()), 200


@company_bp.post("/")
@jwt_required()
def create_company():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    if not name:
        return jsonify({"error": "Field 'name' is required."}), 400

    company = Company(
        name=name.strip(),
        industry=data.get("industry"),
        website=data.get("website"),
    )

    db.session.add(company)
    db.session.commit()

    return jsonify(
        {
            "message": "Company created successfully.",
            "company": company.to_dict(),
        }
    ), 201