# crm-lite-api

Authenticated CRM backend API built with Flask, JWT, SQLAlchemy, and PostgreSQL.

## Features

- User registration and login
- JWT-protected routes
- Lead management
- Company management
- Pipeline stages
- Notes
- Activities
- User-owned data access control

## Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- PostgreSQL
- SQLAlchemy
- Flask-Migrate

## Project Structure

```text
app/
  models/
  routes/
run.py
requirements.txt

How to Run
1. Create a PostgreSQL database
2. Add your connection string to .env
3. Install dependencies:

pip install -r requirements.txt

4. Run migrations:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

5. Start the app:

python run.py

Main Endpoints
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
GET /api/leads/
POST /api/leads/
GET /api/notes/lead/<lead_id>
GET /api/activities/lead/<lead_id>
Future Improvements
Search and filtering
Pagination
Tests
Docker
Deployment

Then push the change:

```bash
git add .
git commit -m "Add project README"
git push

