from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import PipelineStage

stage_bp = Blueprint("stage_bp", __name__)


@stage_bp.get("/")
@jwt_required()
def get_stages():
    stages = PipelineStage.query.order_by(PipelineStage.order_index.asc()).all()
    return jsonify([stage.to_dict() for stage in stages]), 200


@stage_bp.post("/")
@jwt_required()
def create_stage():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    order_index = data.get("order_index")

    if not name:
        return jsonify({"error": "Field 'name' is required."}), 400
    if order_index is None:
        return jsonify({"error": "Field 'order_index' is required."}), 400

    existing_stage = PipelineStage.query.filter_by(name=name.strip()).first()
    if existing_stage:
        return jsonify({"error": "Stage with this name already exists."}), 409

    stage = PipelineStage(
        name=name.strip(),
        order_index=order_index,
    )

    db.session.add(stage)
    db.session.commit()

    return jsonify(
        {
            "message": "Stage created successfully.",
            "stage": stage.to_dict(),
        }
    ), 201