# DentOS Security Model

---

## Overview

DentOS handles sensitive patient health information. This document defines the security controls implemented to protect data confidentiality, integrity, and availability.

---

## Authentication

### User Authentication

| Aspect | Implementation |
|--------|----------------|
| Method | Username + Password |
| Password Storage | bcrypt hash (cost factor 12) |
| Session | JWT tokens |
| Token Expiry | 8 hours |
| Inactivity Timeout | 15 minutes |

### Login Flow

```
User → Enter credentials → Backend validates → Issue JWT → Store in httpOnly cookie
```

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one number
- No password reuse (last 5 passwords)

---

## Authorization

### Role-Based Access Control (RBAC)

| Role | Description |
|------|-------------|
| Receptionist | Front desk operations |
| Dentist | Clinical operations |
| Admin | Full system access |

### Permission Matrix

| Resource | Receptionist | Dentist | Admin |
|----------|--------------|---------|-------|
| Patients - View | Yes | Yes | Yes |
| Patients - Create/Edit | Yes | Yes | Yes |
| Appointments - Manage | Yes | Yes | Yes |
| Visits - View | No | Yes | Yes |
| Visits - Create/Edit | No | Yes | Yes |
| Dental Chart | No | Yes | Yes |
| Prescriptions | No | Yes | Yes |
| Treatment Plans | No | Yes | Yes |
| Billing - Create | Yes | Yes | Yes |
| Billing - Void/Cancel | No | No | Yes |
| Documents - Upload | Yes | Yes | Yes |
| Documents - Delete | No | No | Yes |
| Reports - View | Limited | Limited | Yes |
| Users - Manage | No | No | Yes |
| Settings | No | No | Yes |
| Backup - Manage | No | No | Yes |

---

## Audit Trail

### Audited Events

| Category | Events |
|----------|--------|
| Authentication | Login, Logout, Failed Login |
| Patient | Create, Update, Delete |
| Clinical | Visit Create, Diagnosis Update, Prescription Create |
| Billing | Invoice Create, Payment Record, Invoice Cancel |
| Documents | Upload, Delete |
| Admin | User Create, Role Change, Settings Change |

### Audit Log Fields

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "123",
  "user_name": "dr.smith",
  "action": "PATIENT_UPDATE",
  "resource_type": "Patient",
  "resource_id": "456",
  "changes": {
    "mobile": {"old": "9876543210", "new": "9876543211"}
  },
  "ip_address": "192.168.1.100"
}
```

### Audit Retention

- Audit logs retained for 7 years (regulatory requirement)
- Logs are append-only (no modification/deletion)

---

## Data Protection

### Data at Rest

| Data | Protection |
|------|------------|
| Database | PostgreSQL with local access only |
| Documents | File system permissions |
| Backups | AES-256 encryption |

### Data in Transit

| Communication | Protection |
|---------------|------------|
| Browser ↔ Backend | HTTPS (TLS 1.2+) on local network |
| Backup Upload | HTTPS to cloud provider |

### Sensitive Data Handling

| Data Type | Handling |
|-----------|----------|
| Passwords | Never stored in plain text, bcrypt hashed |
| Patient Medical Data | Access logged, role-restricted |
| Financial Data | Access logged, restricted to billing roles |

---

## Session Management

### Session Security

- JWT stored in httpOnly cookie (not localStorage)
- Secure flag set when using HTTPS
- SameSite=Strict to prevent CSRF
- Token refresh before expiry

### Session Termination

- Explicit logout
- Inactivity timeout (15 minutes)
- Token expiry (8 hours)
- Admin can force logout all sessions

---

## Backup Security

### Backup Encryption

```
Database Dump + Documents
        ↓
    ZIP Archive
        ↓
  AES-256 Encryption
        ↓
    Upload to Cloud
```

### Encryption Key Management

- Encryption key derived from clinic-specific passphrase
- Passphrase set during initial setup
- Passphrase required for restore

---

## Network Security

### Local Network Only (MVP)

- Application binds to local network interface
- No public internet exposure
- Firewall rules recommended

### Future: Remote Access

- VPN or secure tunnel required
- Additional authentication layer
- IP whitelisting

---

## Compliance Considerations

### Data Retention

- Patient records: As per local healthcare regulations (typically 7-10 years)
- Audit logs: 7 years
- Backups: 90 days rolling

### Data Export

- Patient can request data export
- Admin can export all patient data
- Export includes all records, documents, history

### Data Deletion

- Soft delete by default (mark as inactive)
- Hard delete requires Admin + audit log entry
- Backups may retain deleted data per retention policy

---

## Security Checklist (MVP)

- [ ] Password hashing implemented
- [ ] JWT authentication working
- [ ] Role-based access enforced
- [ ] Audit logging active
- [ ] Session timeout configured
- [ ] Backup encryption enabled
- [ ] HTTPS configured for local network

---

## Related Documents

- [Architecture Overview](overview.md)
- [API Specification](api-spec.md)
