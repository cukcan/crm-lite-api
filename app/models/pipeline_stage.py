from app.extensions import db


class PipelineStage(db.Model):
    __tablename__ = "pipeline_stages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    order_index = db.Column(db.Integer, nullable=False)

    leads = db.relationship("Lead", backref="stage", lazy=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "order_index": self.order_index,
        }