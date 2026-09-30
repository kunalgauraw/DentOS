# DentOS

**Dental Practice Management System**

A standalone Windows application for managing dental clinic operations - patients, consultations, prescriptions, and billing.

---

## Features

- **Patient Management** - Register, search, view patient profiles
- **Consultations** - Clinical notes, vitals, follow-ups
- **Prescriptions** - Create and print prescriptions
- **Billing** - Invoices, payments, GST support
- **Reports** - Daily collection, outstanding payments
- **Offline-First** - Works without internet
- **Easy Backup** - Single file database

---

## Project Status

| Phase | Status |
|-------|--------|
| Phase 0: Documentation & Mockup | ✅ Complete |
| Phase 1: MVP Development | 🔄 In Progress |
| Phase 2: Production Build | Not Started |

---

## Quick Links

| Resource | Link |
|----------|------|
| **Live Mockup** | https://kunalgauraw.github.io/DentOS/mockup/ |
| **Documentation** | [docs/](docs/) |
| **Architecture** | [docs/architecture/overview.md](docs/architecture/overview.md) |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript |
| Backend | Python, FastAPI |
| Database | SQLite |
| Desktop | Electron (for .exe) |

---

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+

### Run Locally

```bash
# 1. Start Backend
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# 2. Start Frontend (new terminal)
cd frontend
npm install
npm run dev
```

The SQLite database is created at `data/dentos.db` on first run (path is absolute, independent of the working directory).

### Run Tests

```bash
# Backend (86 tests)
cd backend
python -m pytest tests/ -q

# Frontend (11 tests)
cd frontend
npm run test:run
```

### Access

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Default Login

- **Username:** admin
- **Password:** admin123

---

## Project Structure

```
DentOS/
├── docs/                    # Documentation
│   ├── product/             # Vision, goals, scope, roadmap
│   ├── requirements/        # PRD, user stories
│   └── architecture/        # Technical design
├── mockup/                  # Static HTML mockup
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│   │   └── core/            # Config, security
│   └── requirements.txt
├── frontend/                # React application
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Shared components
│   │   ├── services/        # API client
│   │   └── context/         # Auth context
│   └── package.json
└── data/                    # SQLite database (gitignored)
```

---

## Production Build

The final product will be a standalone Windows installer (`DentOS-Setup.exe`) that:
- Runs without Python/Node installed
- Uses embedded SQLite database
- Works completely offline
- Easy backup (copy single file)

---

## Documentation

| Document | Description |
|----------|-------------|
| [Product Vision](docs/product/vision.md) | Why we're building DentOS |
| [Product Scope](docs/product/scope.md) | MVP features |
| [Architecture](docs/architecture/overview.md) | System design |
| [Database Schema](docs/architecture/database-schema.md) | Data model |
| [API Spec](docs/architecture/api-spec.md) | REST endpoints |

---

## License

Proprietary - Gauravam Denta Clinic

---

## Contact

Dr. Aditya Gaurav  
Gauravam Dental Clinic  
Chapra, Bihar