# DentOS API Specification

---

## Overview

This document defines the REST API endpoints for DentOS. The API follows RESTful conventions and uses JSON for request/response bodies.

---

## Base URL

```
http://localhost:8000/api/v1
```

---

## Authentication

All endpoints except `/auth/login` require authentication via JWT token.

### Headers

```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

---

## Common Response Formats

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "mobile", "message": "Mobile number is required" }
    ]
  }
}
```

### Pagination

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 127,
    "total_pages": 7
  }
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid input data |
| UNAUTHORIZED | 401 | Missing or invalid token |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource conflict (e.g., duplicate) |
| INTERNAL_ERROR | 500 | Server error |

---

## Endpoints

### Authentication

#### POST /auth/login

Login and get JWT token.

**Request:**
```json
{
  "username": "dr.smith",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_at": "2024-01-15T18:00:00Z",
    "user": {
      "id": "uuid",
      "username": "dr.smith",
      "name": "Dr. Smith",
      "role": "DENTIST"
    }
  }
}
```

#### POST /auth/logout

Logout and invalidate token.

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### GET /auth/me

Get current user info.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "username": "dr.smith",
    "name": "Dr. Smith",
    "role": "DENTIST",
    "email": "dr.smith@clinic.com"
  }
}
```

---

### Patients

#### GET /patients

List patients with pagination and search.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| search | string | Search by name, mobile, patient_number |
| page | integer | Page number (default: 1) |
| per_page | integer | Items per page (default: 20, max: 100) |
| is_active | boolean | Filter by active status |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "patient_number": "PAT-000123",
      "name": "John Doe",
      "mobile": "9876543210",
      "gender": "MALE",
      "age": 35,
      "last_visit_date": "2024-01-15"
    }
  ],
  "pagination": { ... }
}
```

#### POST /patients

Create new patient.

**Request:**
```json
{
  "name": "John Doe",
  "mobile": "9876543210",
  "gender": "MALE",
  "date_of_birth": "1989-05-15",
  "address": "123 Main St",
  "email": "john@email.com",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "9876543211",
  "allergies": "Penicillin",
  "medical_conditions": "Diabetes",
  "current_medications": "Metformin 500mg"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "patient_number": "PAT-000124",
    "name": "John Doe",
    ...
  },
  "message": "Patient created successfully"
}
```

#### GET /patients/{id}

Get patient details.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "patient_number": "PAT-000123",
    "name": "John Doe",
    "mobile": "9876543210",
    "gender": "MALE",
    "date_of_birth": "1989-05-15",
    "age": 35,
    "address": "123 Main St",
    "email": "john@email.com",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "9876543211",
    "allergies": "Penicillin",
    "medical_conditions": "Diabetes",
    "current_medications": "Metformin 500mg",
    "is_active": true,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-15T14:30:00Z"
  }
}
```

#### PUT /patients/{id}

Update patient.

**Request:**
```json
{
  "mobile": "9876543212",
  "address": "456 New St"
}
```

**Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Patient updated successfully"
}
```

#### GET /patients/{id}/timeline

Get patient timeline (visits, prescriptions, invoices, documents).

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number |
| per_page | integer | Items per page |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "type": "VISIT",
      "id": "uuid",
      "date": "2024-01-15T10:00:00Z",
      "summary": "Chief Complaint: Tooth pain",
      "details": { ... }
    },
    {
      "type": "PRESCRIPTION",
      "id": "uuid",
      "date": "2024-01-15T10:30:00Z",
      "summary": "RX-000456 - 3 medicines",
      "details": { ... }
    },
    {
      "type": "INVOICE",
      "id": "uuid",
      "date": "2024-01-15T11:00:00Z",
      "summary": "INV-000789 - ₹8,000",
      "details": { ... }
    }
  ],
  "pagination": { ... }
}
```

---

### Appointments

#### GET /appointments

List appointments.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| date | date | Filter by date (YYYY-MM-DD) |
| start_date | date | Filter from date |
| end_date | date | Filter to date |
| patient_id | uuid | Filter by patient |
| user_id | uuid | Filter by dentist |
| status | string | Filter by status |
| page | integer | Page number |
| per_page | integer | Items per page |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "patient": {
        "id": "uuid",
        "patient_number": "PAT-000123",
        "name": "John Doe"
      },
      "user": {
        "id": "uuid",
        "name": "Dr. Smith"
      },
      "appointment_date": "2024-01-15",
      "appointment_time": "10:00:00",
      "duration_minutes": 30,
      "type": "CONSULTATION",
      "status": "SCHEDULED",
      "notes": null
    }
  ],
  "pagination": { ... }
}
```

#### POST /appointments

Create appointment.

**Request:**
```json
{
  "patient_id": "uuid",
  "user_id": "uuid",
  "appointment_date": "2024-01-20",
  "appointment_time": "10:00:00",
  "duration_minutes": 30,
  "type": "CONSULTATION",
  "notes": "First visit"
}
```

#### PUT /appointments/{id}

Update appointment.

**Request:**
```json
{
  "appointment_date": "2024-01-21",
  "appointment_time": "11:00:00"
}
```

#### PATCH /appointments/{id}/status

Update appointment status.

**Request:**
```json
{
  "status": "WAITING"
}
```

#### DELETE /appointments/{id}

Cancel appointment.

**Request:**
```json
{
  "cancellation_reason": "Patient requested"
}
```

---

### Visits

#### GET /visits

List visits.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| patient_id | uuid | Filter by patient |
| user_id | uuid | Filter by dentist |
| date | date | Filter by date |
| status | string | Filter by status |

#### POST /visits

Create visit (start consultation).

**Request:**
```json
{
  "patient_id": "uuid",
  "appointment_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "visit_number": "VIS-000789",
    "patient_id": "uuid",
    "user_id": "uuid",
    "visit_date": "2024-01-15T10:00:00Z",
    "status": "IN_PROGRESS"
  }
}
```

#### GET /visits/{id}

Get visit details.

#### PUT /visits/{id}

Update visit (clinical notes).

**Request:**
```json
{
  "chief_complaint": "Tooth pain upper right",
  "history": "Pain since 3 days",
  "clinical_findings": "Caries #16",
  "diagnosis": "Dental caries",
  "advice": "Avoid cold food",
  "follow_up_date": "2024-01-22"
}
```

#### PATCH /visits/{id}/complete

Complete visit.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "COMPLETED"
  },
  "message": "Visit completed"
}
```

---

### Dental Chart

#### GET /patients/{patient_id}/dental-chart

Get patient's dental chart.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "tooth_number": 16,
      "status": "CARIES",
      "notes": "Deep cavity",
      "updated_at": "2024-01-15T10:30:00Z",
      "updated_by": "Dr. Smith"
    },
    {
      "tooth_number": 36,
      "status": "RCT",
      "notes": "Completed 2023",
      "updated_at": "2023-06-10T14:00:00Z",
      "updated_by": "Dr. Smith"
    }
  ]
}
```

#### PUT /patients/{patient_id}/dental-chart/{tooth_number}

Update tooth status.

**Request:**
```json
{
  "status": "RCT",
  "notes": "RCT completed"
}
```

---

### Prescriptions

#### POST /prescriptions

Create prescription.

**Request:**
```json
{
  "visit_id": "uuid",
  "medicines": [
    {
      "medicine_name": "Amoxicillin",
      "dosage": "500mg",
      "frequency": "1-0-1",
      "duration": "5 days",
      "instructions": "After food"
    },
    {
      "medicine_name": "Ibuprofen",
      "dosage": "400mg",
      "frequency": "1-0-1",
      "duration": "3 days",
      "instructions": "After food, if pain"
    }
  ],
  "notes": "Complete full course"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "rx_number": "RX-000456",
    "patient_id": "uuid",
    "visit_id": "uuid",
    "medicines": [ ... ],
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### GET /prescriptions/{id}

Get prescription details.

#### GET /prescriptions/{id}/pdf

Download prescription as PDF.

**Response:** Binary PDF file

---

### Treatment Plans

#### POST /treatment-plans

Create treatment plan.

**Request:**
```json
{
  "patient_id": "uuid",
  "visit_id": "uuid",
  "procedures": [
    {
      "procedure_name": "Root Canal Treatment",
      "tooth_number": 16,
      "cost": 8000,
      "sessions": 2,
      "notes": "Two sessions required"
    },
    {
      "procedure_name": "Crown",
      "tooth_number": 16,
      "cost": 5000,
      "sessions": 1,
      "notes": "After RCT"
    }
  ],
  "notes": "Treatment plan for #16"
}
```

#### GET /treatment-plans/{id}

Get treatment plan details.

#### PUT /treatment-plans/{id}

Update treatment plan.

#### PATCH /treatment-plans/{id}/status

Update plan status.

**Request:**
```json
{
  "status": "APPROVED"
}
```

#### PATCH /treatment-plans/{id}/procedures/{procedure_id}/status

Update procedure status.

**Request:**
```json
{
  "status": "COMPLETED"
}
```

---

### Invoices

#### GET /invoices

List invoices.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| patient_id | uuid | Filter by patient |
| status | string | Filter by status |
| start_date | date | Filter from date |
| end_date | date | Filter to date |

#### POST /invoices

Create invoice.

**Request:**
```json
{
  "patient_id": "uuid",
  "treatment_plan_id": "uuid",
  "items": [
    {
      "description": "Consultation Fee",
      "quantity": 1,
      "unit_price": 500
    },
    {
      "procedure_id": "uuid",
      "description": "Root Canal Treatment #16",
      "quantity": 1,
      "unit_price": 8000
    }
  ],
  "discount": 500,
  "notes": "Discount for regular patient"
}
```

#### GET /invoices/{id}

Get invoice details.

#### PATCH /invoices/{id}/issue

Issue invoice (change from DRAFT to ISSUED).

#### PATCH /invoices/{id}/cancel

Cancel invoice (Admin only).

**Request:**
```json
{
  "cancellation_reason": "Duplicate invoice"
}
```

#### GET /invoices/{id}/pdf

Download invoice as PDF.

---

### Payments

#### POST /payments

Record payment.

**Request:**
```json
{
  "invoice_id": "uuid",
  "amount": 5000,
  "payment_mode": "UPI",
  "reference": "TXN123456789",
  "notes": "Partial payment"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "receipt_number": "RCP-000123",
    "invoice_id": "uuid",
    "amount": 5000,
    "payment_mode": "UPI",
    "payment_date": "2024-01-15",
    "reference": "TXN123456789"
  },
  "message": "Payment recorded"
}
```

#### GET /payments/{id}/receipt

Download receipt as PDF.

---

### Documents

#### POST /documents

Upload document.

**Request:** Multipart form data
| Field | Type | Description |
|-------|------|-------------|
| file | file | Document file (JPG, PNG, PDF) |
| patient_id | uuid | Patient ID |
| visit_id | uuid | Visit ID (optional) |
| document_type | string | XRAY, PHOTO, CONSENT, REPORT, OTHER |
| description | string | Description (optional) |

#### GET /documents/{id}

Download document.

#### DELETE /documents/{id}

Delete document (Admin only).

---

### Reports

#### GET /reports/daily-collections

Get daily collections report.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| start_date | date | Start date |
| end_date | date | End date |

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 45000,
    "by_mode": {
      "CASH": 15000,
      "UPI": 25000,
      "CARD": 5000,
      "BANK_TRANSFER": 0
    },
    "transactions": [
      {
        "receipt_number": "RCP-000123",
        "patient_name": "John Doe",
        "amount": 8000,
        "payment_mode": "UPI",
        "time": "10:30:00"
      }
    ]
  }
}
```

#### GET /reports/outstanding

Get outstanding payments report.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_outstanding": 125000,
    "patients": [
      {
        "patient_id": "uuid",
        "patient_name": "John Doe",
        "patient_number": "PAT-000123",
        "outstanding": 3000,
        "invoices": [
          {
            "invoice_number": "INV-000456",
            "total": 8000,
            "paid": 5000,
            "balance": 3000,
            "date": "2024-01-15"
          }
        ]
      }
    ]
  }
}
```

#### GET /reports/follow-ups

Get upcoming follow-ups.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| start_date | date | Start date |
| end_date | date | End date |

---

### Users

#### GET /users

List users (Admin only).

#### POST /users

Create user (Admin only).

**Request:**
```json
{
  "username": "receptionist1",
  "password": "password123",
  "name": "Reception Staff",
  "role": "RECEPTIONIST",
  "email": "reception@clinic.com",
  "phone": "9876543210"
}
```

#### PUT /users/{id}

Update user (Admin only).

#### PATCH /users/{id}/deactivate

Deactivate user (Admin only).

#### PATCH /users/{id}/reset-password

Reset user password (Admin only).

**Request:**
```json
{
  "new_password": "newpassword123"
}
```

---

### Settings

#### GET /settings

Get clinic settings.

#### PUT /settings

Update clinic settings (Admin only).

**Request:**
```json
{
  "clinic_name": "My Dental Clinic",
  "address": "123 Main St",
  "phone": "9876543210",
  "email": "clinic@email.com",
  "prescription_header": "...",
  "invoice_header": "..."
}
```

#### POST /settings/logo

Upload clinic logo.

---

### Backup

#### POST /backup/run

Run manual backup (Admin only).

#### GET /backup/history

Get backup history (Admin only).

#### POST /backup/restore

Restore from backup (Admin only).

---

## Related Documents

- [Architecture Overview](overview.md)
- [Domain Model](domain-model.md)
- [Security Model](security.md)
