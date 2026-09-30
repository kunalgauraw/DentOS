# DentOS

**The Operating System for Modern Dental Clinics**

---

## What is DentOS?

DentOS is a local-first, cloud-backed Dental Practice Management System (PMS) designed for small dental clinics. It enables clinics to manage patient records, consultations, prescriptions, treatment plans, billing, and documents through a single reliable application.

**Key Features:**
- Works offline (local-first architecture)
- Full data ownership
- Automated backups
- Role-based access control
- Print-ready prescriptions, invoices, and receipts

---

## Project Status

| Phase | Status |
|-------|--------|
| Phase 0: Product Definition | In Progress |
| Phase 1: MVP Development | Not Started |
| Phase 2: Operational Efficiency | Not Started |
| Phase 3: Owner Visibility | Not Started |

---

## Documentation

| Document | Description |
|----------|-------------|
| [Product Vision](docs/product/vision.md) | Why we're building DentOS |
| [Goals & Success Criteria](docs/product/goals.md) | What success looks like |
| [Product Scope](docs/product/scope.md) | What's in and out of MVP |
| [Product Roadmap](docs/product/roadmap.md) | Phased delivery plan |
| [Requirements (PRD)](docs/requirements/prd.md) | Detailed functional requirements |
| [Architecture Overview](docs/architecture/overview.md) | System design and tech stack |
| [Security Model](docs/architecture/security.md) | Authentication, authorization, audit |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Material UI |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Deployment | Docker Compose |

---

## Project Structure

```
DentOS/
├── docs/                    # Documentation
│   ├── product/             # Vision, goals, scope, roadmap
│   ├── requirements/        # PRD, user stories, business rules
│   ├── architecture/        # Technical design, API, security
│   ├── operations/          # Installation, backup, user guides
│   └── project/             # Release plans, backlog
├── design/                  # Design artifacts
│   ├── wireframes/          # UI mockups
│   ├── workflows/           # Process flow diagrams
│   └── assets/              # Design source files
├── frontend/                # React application
├── backend/                 # FastAPI application
├── database/                # Migrations and seeds
├── deployment/              # Docker and deployment configs
├── scripts/                 # Utility scripts
└── tests/                   # Integration and E2E tests
```

---

## Getting Started

### Prerequisites

- Docker Desktop
- Git

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd DentOS

# Start development environment
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Contributing

1. Read the [Product Vision](docs/product/vision.md)
2. Check the [Roadmap](docs/product/roadmap.md) for current priorities
3. Review [Architecture](docs/architecture/overview.md) before making changes
4. Follow the coding standards (TBD)

---

## License

TBD

---

## Contact

TBD
