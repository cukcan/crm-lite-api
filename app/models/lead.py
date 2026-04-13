from datetime import datetime
from app.extensions import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    source = db.Column(db.String(80), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="open")
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=True)
    stage_id = db.Column(db.Integer, db.ForeignKey("pipeline_stages.id"), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    notes = db.relationship(
        "Note",
        backref="lead",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="desc(Note.created_at)",
    )

    activities = db.relationship(
        "Activity",
        backref="lead",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="desc(Activity.created_at)",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "source": self.source,
            "status": self.status,
            "company_id": self.company_id,
            "stage_id": self.stage_id,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "company_name": self.company.name if self.company else None,
            "stage_name": self.stage.name if self.stage else None,
            "owner_email": self.owner.email if self.owner else None,
            "notes_count": len(self.notes),
            "activities_count": len(self.activities),
        }