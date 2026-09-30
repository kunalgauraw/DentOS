# DentOS Architecture Overview

---

## System Architecture

### Local-First, Cloud-Backed

```
                    Clinic Network
    ┌────────────────────────────────────────────┐
    │                                            │
    │   ┌─────────────────┐    ┌────────────┐   │
    │   │ Windows Laptop  │    │ Secondary  │   │
    │   │ (Primary Host)  │◄───│ Devices    │   │
    │   │                 │    │ (Browser)  │   │
    │   │ ┌─────────────┐ │    └────────────┘   │
    │   │ │ DentOS App  │ │                     │
    │   │ │ (Frontend)  │ │                     │
    │   │ └──────┬──────┘ │                     │
    │   │        │        │                     │
    │   │ ┌──────▼──────┐ │                     │
    │   │ │ DentOS API  │ │                     │
    │   │ │ (Backend)   │ │                     │
    │   │ └──────┬──────┘ │                     │
    │   │        │        │                     │
    │   │ ┌──────▼──────┐ │                     │
    │   │ │ PostgreSQL  │ │                     │
    │   │ │ (Database)  │ │                     │
    │   │ └─────────────┘ │                     │
    │   │                 │                     │
    │   │ ┌─────────────┐ │                     │
    │   │ │ PatientFiles│ │                     │
    │   │ │ (Documents) │ │                     │
    │   │ └─────────────┘ │                     │
    │   └────────┬────────┘                     │
    │            │                              │
    └────────────┼──────────────────────────────┘
                 │
                 │ Daily Encrypted Backup
                 ▼
         ┌───────────────┐
         │ Cloud Storage │
         │ (OneDrive /   │
         │ Google Drive) │
         └───────────────┘
```

---

## Technology Stack

### Frontend

| Technology | Purpose |
|------------|---------|
| React | UI framework |
| TypeScript | Type safety |
| Material UI | Component library |
| React Router | Navigation |
| React Query | Data fetching & caching |
| Vite | Build tool |

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Runtime |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| Alembic | Database migrations |

### Database

| Technology | Purpose |
|------------|---------|
| PostgreSQL 15+ | Primary database |

### Infrastructure

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Local orchestration |

---

## Device Strategy

### Primary Device: Windows Laptop

Acts as:
- Application Host
- Database Host
- Document Repository
- Backup Source

**Minimum Requirements:**
- Windows 10/11
- 8 GB RAM
- 256 GB Storage
- Intel i5 or equivalent

### Secondary Devices

- Android Phone
- Tablet
- Additional Laptop

Access through browser on local network (same WiFi).

---

## File Storage

### MVP Approach

Store files on local disk:

```
C:\DentOS\
└── PatientFiles\
    └── {PatientID}\
        ├── xrays\
        ├── photos\
        ├── documents\
        └── prescriptions\
```

### Future Consideration

Introduce object storage (MinIO or cloud) only if scale demands it.

---

## Authentication & Authorization

### Authentication

- Custom username/password authentication
- JWT tokens for session management
- Automatic logout after 15 minutes inactivity

### Authorization (Roles)

| Role | Permissions |
|------|-------------|
| Receptionist | Patients, Appointments, Billing, Documents |
| Dentist | All Receptionist + Clinical, Prescriptions, Treatment Plans |
| Admin | All + User Management, Settings, Backup, Reports |

---

## Deployment Model

### Development

```bash
docker-compose up
```

Runs:
- Frontend (React dev server)
- Backend (FastAPI with hot reload)
- Database (PostgreSQL)

### Production (Clinic)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Runs:
- Frontend (Nginx serving static files)
- Backend (FastAPI with Gunicorn)
- Database (PostgreSQL with persistence)

---

## Backup Strategy

### Daily Backup Contents

- PostgreSQL database dump
- Patient documents folder
- Application configuration

### Backup Process

1. Scheduled task runs at configured time (e.g., 11 PM)
2. Database dump created
3. Documents archived
4. Combined archive encrypted
5. Uploaded to cloud storage (OneDrive/Google Drive)
6. Local copy retained for 7 days

### Backup Destinations

| Priority | Destination |
|----------|-------------|
| Primary | OneDrive or Google Drive |
| Optional | External Hard Disk (weekly) |

---

## Security Architecture

### Must Have (MVP)

- [x] User login required
- [x] Role-based permissions
- [x] Audit trail for sensitive operations
- [x] Backup encryption
- [x] Automatic session logout
- [x] Document access control

### Audit Events

Track:
- Patient creation/update
- Diagnosis updates
- Prescription generation
- Invoice creation/cancellation
- Payment collection
- User login/logout

---

## API Design

### REST API Structure

```
/api/v1/
├── /auth
│   ├── POST /login
│   └── POST /logout
├── /patients
│   ├── GET /
│   ├── POST /
│   ├── GET /{id}
│   ├── PUT /{id}
│   └── GET /{id}/timeline
├── /appointments
│   ├── GET /
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── /visits
│   ├── GET /
│   ├── POST /
│   ├── GET /{id}
│   └── PUT /{id}
├── /prescriptions
│   ├── POST /
│   ├── GET /{id}
│   └── GET /{id}/pdf
├── /treatments
│   ├── POST /
│   ├── GET /{id}
│   └── PUT /{id}/status
├── /invoices
│   ├── POST /
│   ├── GET /{id}
│   └── GET /{id}/pdf
├── /payments
│   ├── POST /
│   └── GET /{id}/receipt
├── /documents
│   ├── POST /upload
│   └── GET /{id}
├── /reports
│   ├── GET /daily-collections
│   ├── GET /outstanding
│   └── GET /follow-ups
└── /users
    ├── GET /
    ├── POST /
    └── PUT /{id}
```

---

## Related Documents

- [Domain Model](domain-model.md)
- [API Specification](api-spec.md)
- [Security Model](security.md)
- [Database Schema](database-schema.md)
- [Architecture Decisions](decisions/)
