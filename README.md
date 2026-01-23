# NEKETS — Simple User CRUD with FastAPI

This is a small but fully functional CRUD application for managing users.  
The backend is built with modern async FastAPI + SQLAlchemy 2.0, database is PostgreSQL, and the frontend is pure vanilla JavaScript with no frameworks.  
The project is lightweight, fast, and completely asynchronous — no blocking operations. 

## ✨ Features

- **Full async stack**: async engine, async sessions, async routes  
- **UUID as primary key** — modern and secure  
- **Data validation** via Pydantic (with constraints and descriptions). 
- **RESTful API** with proper status codes and response models  
- **Simple frontend** in `public/index.html` — list users, add, edit, delete right in the browser  
- Automatic table creation on startup  
- OpenAPI docs at `/docs` and `/redoc`

## 🛠 Tech Stack

- **FastAPI**  
- **SQLAlchemy 2.0** 
- **PostgreSQL** 
- **Pydantic v2**  
- **python-dotenv** for environment variables  
- **Uvicorn** for running the server  
- Vanilla HTML + CSS + JavaScript (no React/Vue)

## 🎨 Frontend

Everything is in a single file `public/index.html`:
- Table with the list of users  
- Form for adding/editing  
- Edit and Delete buttons in each row  

## 🚀 How to Run

### Dependencies and Lockfile

This project uses **[uv](https://docs.astral.sh/uv/)** — an extremely fast Python package manager and resolver — to manage dependencies.

- Dependencies are declared in `pyproject.toml`.
- Exact versions (including transitive dependencies) are pinned in `uv.lock` for full reproducibility.

**Recommended way to install dependencies:**
 
```bash
# Install uv if you don't have it yet
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip: pip install uv

# Then sync the environment (creates/uses .venv and installs exactly what's in uv.lock)
uv sync
```
This guarantees the same environment on any machine or CI/CD.
Alternative (classic pip): 
```
pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv
```

### 2. Set up the database

Create a database in PostgreSQL and add a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/your_db_name
```

### 3. Run the app

```bash
uvicorn simple_api:app --reload
```

Open in your browser: http://127.0.0.1:8000
API documentation: http://127.0.0.1:8000/docs

## 📡 API Endpoints

| Method | Path                     | Description                       |
|--------|--------------------------|-----------------------------------|
| GET    | `/`                      | Main page (index.html)            |
| GET    | `/api/users/`            | Get all users                     |
| GET    | `/api/users/{user_id}`   | Get user by UUID                  |
| POST   | `/api/users`             | Create new user                   |
| PUT    | `/api/users/{user_id}`   | Update user (partial)             |
| DELETE | `/api/users/{user_id}`   | Delete user                       |

### Example requests (curl)

**Create user**
```bash
curl -X POST http://127.0.0.1:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Neket", "age": 22}'
```

**Update user**
```bash
curl -X PUT http://127.0.0.1:8000/api/users/550e8400-e29b-41d4-a716-446655440032 \
  -H "Content-Type: application/json" \
  -d '{"name": "Neket"}'
```
