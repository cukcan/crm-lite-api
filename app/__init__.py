from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt
from app.routes.auth_routes import auth_bp
from app.routes.lead_routes import lead_bp
from app.routes.company_routes import company_bp
from app.routes.stage_routes import stage_bp
from app.routes.note_routes import note_bp
from app.routes.activity_routes import activity_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(company_bp, url_prefix="/api/companies")
    app.register_blueprint(stage_bp, url_prefix="/api/stages")
    app.register_blueprint(lead_bp, url_prefix="/api/leads")
    app.register_blueprint(note_bp, url_prefix="/api/notes")
    app.register_blueprint(activity_bp, url_prefix="/api/activities")

    @app.get("/")
    def home():
        return jsonify(
            {
                "message": "crm-lite-api is running",
                "endpoints": {
                    "auth_register": "/api/auth/register",
                    "auth_login": "/api/auth/login",
                    "auth_me": "/api/auth/me",
                    "companies": "/api/companies/",
                    "stages": "/api/stages/",
                    "leads": "/api/leads/",
                    "notes_for_lead": "/api/notes/lead/<lead_id>",
                    "activities_for_lead": "/api/activities/lead/<lead_id>",
                },
            }
        )

    return app