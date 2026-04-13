🚀 crm-lite-api

Authenticated CRM backend API built with Flask, JWT, and PostgreSQL, designed to simulate real-world business workflows.

📌 Overview

crm-lite-api is a backend system that combines authentication and customer relationship management (CRM) features into a single application.

It allows users to:

Register and log in securely
Manage leads and companies
Track sales pipeline stages
Add notes and activities to leads
Access only their own data (user-based ownership)

This project is inspired by real ERP/CRM systems such as Odoo.

⚙️ Features
🔐 Authentication
User registration & login
JWT-based authentication
Protected API routes
📊 CRM Core
Lead management (CRUD)
Company management
Pipeline stages (sales flow)
📝 Notes
Add notes to leads
Update and delete notes
Retrieve notes per lead
📅 Activities
Schedule activities (call, meeting, demo, etc.)
Mark activities as completed
Track follow-ups
🔒 Security
User-based data ownership
Access control via JWT
Password hashing
🛠️ Tech Stack
Python
Flask
Flask-JWT-Extended
PostgreSQL
SQLAlchemy
Flask-Migrate
📂 Project Structure
crm-lite-api/
├── app/
│   ├── models/        # Database models
│   ├── routes/        # API endpoints
│   ├── config.py      # Configuration
│   ├── extensions.py  # DB & JWT setup
│   └── __init__.py    # App factory
├── run.py             # Entry point
├── requirements.txt
├── .env
└── README.md
🚀 Getting Started
1. Clone the repository
git clone https://github.com/cukcan/crm-lite-api
cd crm-lite-api
2. Create virtual environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/crm_lite_db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
5. Setup database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
6. Run the application
python run.py

Server runs at:

http://127.0.0.1:5000
📡 API Endpoints
🔐 Auth
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
📊 Leads
GET /api/leads/
POST /api/leads/
PUT /api/leads/<id>
DELETE /api/leads/<id>
🏢 Companies
GET /api/companies/
POST /api/companies/
🔄 Pipeline Stages
GET /api/stages/
POST /api/stages/
📝 Notes
GET /api/notes/lead/<lead_id>
POST /api/notes/lead/<lead_id>
PUT /api/notes/<id>
DELETE /api/notes/<id>
📅 Activities
GET /api/activities/lead/<lead_id>
POST /api/activities/lead/<lead_id>
PUT /api/activities/<id>
DELETE /api/activities/<id>
🧠 Design Decisions
Single application architecture → simpler and practical for small systems
JWT authentication → stateless and scalable
User-based ownership model → realistic access control
Modular structure → easy to extend and maintain
🔮 Future Improvements
Search & filtering (e.g. by stage, status)
Pagination for large datasets
Role-based access control (admin/user)
API documentation (Swagger/OpenAPI)
Unit & integration tests
Docker support
Deployment (Render / Railway)
📈 Use Cases
Backend for CRM or SaaS applications
Learning project for backend development
Demonstration of real-world API design
Foundation for larger ERP-style systems
👨‍💻 Author

Ibrahim Bitikcioglu
📍 Istanbul, Turkey
🔗 https://github.com/cukcan
