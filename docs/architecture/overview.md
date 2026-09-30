# DentOS Architecture Overview

---

## System Architecture

### Standalone Windows Application

DentOS is designed as a **standalone Windows desktop application** that runs entirely on a single PC without requiring Docker, cloud services, or complex infrastructure.

```
    ┌─────────────────────────────────────────────────────┐
    │              Windows PC (Clinic)                    │
    │                                                     │
    │   ┌─────────────────────────────────────────────┐   │
    │   │           DentOS.exe                        │   │
    │   │   ┌─────────────────────────────────────┐   │   │
    │   │   │         React Frontend              │   │   │
    │   │   │        (Embedded Browser)           │   │   │
    │   │   └──────────────┬──────────────────────┘   │   │
    │   │                  │ HTTP (localhost)         │   │
    │   │   ┌──────────────▼──────────────────────┐   │   │
    │   │   │         FastAPI Backend             │   │   │
    │   │   │        (Embedded Server)            │   │   │
    │   │   └──────────────┬──────────────────────┘   │   │
    │   │                  │                          │   │
    │   │   ┌──────────────▼──────────────────────┐   │   │
    │   │   │         SQLite Database             │   │   │
    │   │   │        (Single File)                │   │   │
    │   │   └─────────────────────────────────────┘   │   │
    │   └─────────────────────────────────────────────┘   │
    │                                                     │
    │   ┌─────────────────────────────────────────────┐   │
    │   │  C:\DentOS\                                 │   │
    │   │  ├── data\dentos.db    (Database)           │   │
    │   │  ├── backups\          (Daily backups)      │   │
    │   │  └── documents\        (Patient files)      │   │
    │   └─────────────────────────────────────────────┘   │
    │                                                     │
    └──────────────────────┬──────────────────────────────┘
                           │
                           │ Manual/Scheduled Backup
                           ▼
                   ┌───────────────┐
                   │ External Drive│
                   │ or Cloud Sync │
                   │ (OneDrive)    │
                   └───────────────┘
```

---

## Deployment Model

### Single Executable Approach

| Component | Technology | Packaging |
|-----------|------------|-----------|
| Frontend | React + TypeScript | Bundled with Electron |
| Backend | FastAPI + Python | Packaged with PyInstaller |
| Database | SQLite | Single file (no server) |
| Desktop Shell | Electron | Creates .exe installer |

### How It Works

1. **User double-clicks DentOS.exe**
2. Electron starts embedded browser window
3. Backend server starts on localhost:8000
4. Frontend loads in Electron window
5. All data stored in `C:\DentOS\data\`

### No Dependencies Required

The clinic PC does NOT need:
- ❌ Python installed
- ❌ Node.js installed
- ❌ Docker installed
- ❌ Database server
- ❌ Internet connection (for daily use)

---

## Technology Stack

### Frontend

| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| Electron | Desktop wrapper |

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Runtime |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| PyInstaller | Creates standalone .exe |

### Database

| Technology | Purpose |
|------------|---------|
| SQLite | Embedded database (single file) |

**Why SQLite?**
- No separate database server needed
- Single file = easy backup
- Perfect for single-clinic use
- Can handle thousands of patients

---

## Development vs Production

### Development (Your PC)

```
Terminal 1: cd backend && python -m uvicorn app.main:app --reload
Terminal 2: cd frontend && npm run dev
```

Access at: http://localhost:5173

### Production (Clinic PC)

```
Double-click: DentOS-Setup.exe
```

Installs to: `C:\Program Files\DentOS\`
Data stored in: `C:\DentOS\`

---

## File Storage

### Data Directory Structure

```
C:\DentOS\
├── data\
│   └── dentos.db           # SQLite database
├── documents\
│   └── {PatientID}\
│       ├── xrays\
│       ├── photos\
│       └── prescriptions\
├── backups\
│   ├── backup_2024-01-15.zip
│   └── backup_2024-01-14.zip
└── logs\
    └── dentos.log
```

---

## Authentication & Authorization

### Authentication

- Username/password login
- JWT tokens for session management
- Automatic logout after 8 hours (configurable)

### Authorization (Roles)

| Role | Permissions |
|------|-------------|
| Admin | Full access + User management + Settings |
| Dentist | Clinical + Billing + Reports |
| Visiting Dentist | Clinical (own patients) + Billing (no discount) |
| Receptionist | Patients + Appointments + Billing + Daily collection |

---

## Backup Strategy

### Automatic Daily Backup

1. Scheduled task runs at configured time (e.g., 11 PM)
2. SQLite database copied
3. Documents folder archived
4. Combined into single ZIP file
5. Stored in `C:\DentOS\backups\`
6. Old backups deleted after retention period (default: 30 days)

### Backup Destinations

| Priority | Destination | Method |
|----------|-------------|--------|
| Primary | Local backups folder | Automatic |
| Secondary | OneDrive/Google Drive | Sync folder |
| Optional | External USB drive | Manual copy |

### Restore Process

1. Stop DentOS
2. Replace `dentos.db` with backup
3. Restore documents folder
4. Start DentOS

---

## Security

### Must Have (MVP)

- [x] User login required
- [x] Role-based permissions
- [x] Password hashing (bcrypt)
- [x] JWT token authentication
- [x] Automatic session timeout

### Data Protection

- Database is local (not on internet)
- Backups can be encrypted (future)
- No patient data sent to cloud (except backups)

---

## System Requirements

### Minimum (Clinic PC)

| Component | Requirement |
|-----------|-------------|
| OS | Windows 10/11 |
| RAM | 4 GB |
| Storage | 50 GB free |
| Processor | Any modern CPU |
| Display | 1366x768 minimum |

### Recommended

| Component | Requirement |
|-----------|-------------|
| OS | Windows 11 |
| RAM | 8 GB |
| Storage | 256 GB SSD |
| Display | 1920x1080 |

---

## Build & Distribution

### Build Process

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Package backend
cd backend
pyinstaller --onefile app/main.py

# 3. Create Electron installer
cd electron
npm run make
```

### Output

```
dist/
└── DentOS-Setup-1.0.0.exe    # Windows installer (~100 MB)
```

### Installation

1. Run `DentOS-Setup-1.0.0.exe`
2. Follow installer wizard
3. Launch from Start Menu or Desktop shortcut

---

## Future Considerations

### Multi-Device Access (Phase 2)

If needed, the backend can serve other devices on the same network:
- Tablet at reception
- Phone for quick lookups
- Access via browser at `http://192.168.x.x:8000`

### Cloud Sync (Phase 3)

Optional cloud features:
- Automatic backup to cloud
- Multi-clinic data sync
- Remote access

---

## Related Documents

- [Domain Model](domain-model.md)
- [API Specification](api-spec.md)
- [Security Model](security.md)
- [Database Schema](database-schema.md)
