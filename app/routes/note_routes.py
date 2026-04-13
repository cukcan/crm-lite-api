from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Lead, Note

note_bp = Blueprint("note_bp", __name__)


def get_owned_lead_or_404(lead_id: int, user_id: int):
    lead = Lead.query.filter_by(id=lead_id, owner_id=user_id).first()
    if not lead:
        return None
    return lead


@note_bp.get("/lead/<int:lead_id>")
@jwt_required()
def get_notes_for_lead(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = get_owned_lead_or_404(lead_id, current_user_id)

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    notes = Note.query.filter_by(lead_id=lead.id).order_by(Note.created_at.desc()).all()
    return jsonify([note.to_dict() for note in notes]), 200


@note_bp.get("/<int:note_id>")
@jwt_required()
def get_note(note_id: int):
    current_user_id = int(get_jwt_identity())

    note = (
        Note.query.join(Lead, Note.lead_id == Lead.id)
        .filter(Note.id == note_id, Lead.owner_id == current_user_id)
        .first()
    )

    if not note:
        return jsonify({"error": "Note not found."}), 404

    return jsonify(note.to_dict()), 200


@note_bp.post("/lead/<int:lead_id>")
@jwt_required()
def create_note(lead_id: int):
    current_user_id = int(get_jwt_identity())
    lead = get_owned_lead_or_404(lead_id, current_user_id)

    if not lead:
        return jsonify({"error": "Lead not found."}), 404

    data = request.get_json(silent=True) or {}
    content = data.get("content")

    if not content or not content.strip():
        return jsonify({"error": "Field 'content' is required."}), 400

    note = Note(
        lead_id=lead.id,
        content=content.strip(),
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(
        {
            "message": "Note created successfully.",
            "note": note.to_dict(),
        }
    ), 201


@note_bp.put("/<int:note_id>")
@jwt_required()
def update_note(note_id: int):
    current_user_id = int(get_jwt_identity())

    note = (
        Note.query.join(Lead, Note.lead_id == Lead.id)
        .filter(Note.id == note_id, Lead.owner_id == current_user_id)
        .first()
    )

    if not note:
        return jsonify({"error": "Note not found."}), 404

    data = request.get_json(silent=True) or {}
    content = data.get("content")

    if content is None or not str(content).strip():
        return jsonify({"error": "Field 'content' is required."}), 400

    note.content = str(content).strip()
    db.session.commit()

    return jsonify(
        {
            "message": "Note updated successfully.",
            "note": note.to_dict(),
        }
    ), 200


@note_bp.delete("/<int:note_id>")
@jwt_required()
def delete_note(note_id: int):
    current_user_id = int(get_jwt_identity())

    note = (
        Note.query.join(Lead, Note.lead_id == Lead.id)
        .filter(Note.id == note_id, Lead.owner_id == current_user_id)
        .first()
    )

    if not note:
        return jsonify({"error": "Note not found."}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully."}), 200