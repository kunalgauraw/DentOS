# DentOS Domain Model

---

## Overview

This document defines the core entities, their attributes, and relationships in DentOS.

---

## Entity Relationship Diagram (ERD)

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │   Patient   │       │ Appointment │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │       │ id          │◄──────│ patient_id  │
│ username    │       │ name        │       │ user_id     │──────┐
│ password    │       │ mobile      │       │ date_time   │      │
│ role        │       │ dob         │       │ status      │      │
│ name        │       │ gender      │       │ type        │      │
│ email       │       │ address     │       │ notes       │      │
│ is_active   │       │ email       │       └─────────────┘      │
└──────┬──────┘       │ emergency   │                            │
       │              │ allergies   │       ┌─────────────┐      │
       │              │ conditions  │       │    Visit    │      │
       │              │ medications │       ├─────────────┤      │
       │              │ created_at  │◄──────│ patient_id  │      │
       │              └──────┬──────┘       │ user_id     │──────┤
       │                     │              │ appointment │      │
       │                     │              │ chief_comp  │      │
       │                     │              │ history     │      │
       │                     │              │ findings    │      │
       │                     │              │ diagnosis   │      │
       │                     │              │ advice      │      │
       │                     │              │ follow_up   │      │
       │                     │              │ created_at  │      │
       │                     │              └──────┬──────┘      │
       │                     │                     │             │
       │    ┌────────────────┼─────────────────────┤             │
       │    │                │                     │             │
       │    ▼                ▼                     ▼             │
       │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
       │  │ DentalChart │  │ Prescription│  │TreatmentPlan│      │
       │  ├─────────────┤  ├─────────────┤  ├─────────────┤      │
       │  │ patient_id  │  │ visit_id    │  │ patient_id  │      │
       │  │ tooth_num   │  │ patient_id  │  │ visit_id    │      │
       │  │ status      │  │ user_id     │  │ created_by  │──────┤
       │  │ notes       │  │ rx_number   │  │ status      │      │
       │  │ updated_at  │  │ created_at  │  │ total_cost  │      │
       │  │ updated_by  │  └──────┬──────┘  │ created_at  │      │
       │  └─────────────┘         │         └──────┬──────┘      │
       │                          │                │             │
       │                          ▼                ▼             │
       │                 ┌─────────────┐  ┌─────────────┐        │
       │                 │  Medicine   │  │  Procedure  │        │
       │                 ├─────────────┤  ├─────────────┤        │
       │                 │ rx_id       │  │ plan_id     │        │
       │                 │ name        │  │ name        │        │
       │                 │ dosage      │  │ tooth_num   │        │
       │                 │ frequency   │  │ cost        │        │
       │                 │ duration    │  │ sessions    │        │
       │                 │ instructions│  │ status      │        │
       │                 └─────────────┘  │ notes       │        │
       │                                  └──────┬──────┘        │
       │                                         │               │
       │                     ┌───────────────────┘               │
       │                     │                                   │
       │                     ▼                                   │
       │              ┌─────────────┐       ┌─────────────┐      │
       │              │   Invoice   │       │   Payment   │      │
       │              ├─────────────┤       ├─────────────┤      │
       │              │ patient_id  │◄──────│ invoice_id  │      │
       └──────────────│ created_by  │       │ amount      │      │
                      │ inv_number  │       │ mode        │      │
                      │ total       │       │ receipt_num │      │
                      │ paid        │       │ created_by  │──────┘
                      │ balance     │       │ created_at  │
                      │ status      │       └─────────────┘
                      │ created_at  │
                      └──────┬──────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ InvoiceItem │
                      ├─────────────┤
                      │ invoice_id  │
                      │ procedure_id│
                      │ description │
                      │ amount      │
                      └─────────────┘


       ┌─────────────┐       ┌─────────────┐
       │  Document   │       │  AuditLog   │
       ├─────────────┤       ├─────────────┤
       │ patient_id  │       │ user_id     │
       │ visit_id    │       │ action      │
       │ type        │       │ entity_type │
       │ file_path   │       │ entity_id   │
       │ file_name   │       │ changes     │
       │ uploaded_by │       │ ip_address  │
       │ uploaded_at │       │ created_at  │
       └─────────────┘       └─────────────┘
```

---

## Core Entities

### User

Represents clinic staff who use the system.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| username | String(50) | Yes | Unique login name |
| password_hash | String(255) | Yes | Bcrypt hashed password |
| role | Enum | Yes | RECEPTIONIST, DENTIST, ADMIN |
| name | String(100) | Yes | Display name |
| email | String(100) | No | Email address |
| phone | String(15) | No | Contact number |
| is_active | Boolean | Yes | Account status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Last update timestamp |

---

### Patient

Represents a patient registered at the clinic.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| patient_number | String(20) | Yes | Unique patient ID (e.g., PAT-0001) |
| name | String(100) | Yes | Full name |
| mobile | String(15) | Yes | Primary contact |
| date_of_birth | Date | No | DOB |
| age | Integer | No | Age (if DOB not known) |
| gender | Enum | Yes | MALE, FEMALE, OTHER |
| address | Text | No | Full address |
| email | String(100) | No | Email address |
| emergency_contact_name | String(100) | No | Emergency contact name |
| emergency_contact_phone | String(15) | No | Emergency contact number |
| allergies | Text | No | Known allergies |
| medical_conditions | Text | No | Existing conditions |
| current_medications | Text | No | Current medications |
| notes | Text | No | General notes |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Registration date |
| updated_at | DateTime | Yes | Last update |
| created_by | UUID | Yes | FK to User |

---

### Appointment

Represents a scheduled appointment.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| patient_id | UUID | Yes | FK to Patient |
| user_id | UUID | No | FK to User (assigned dentist) |
| appointment_date | Date | Yes | Appointment date |
| appointment_time | Time | Yes | Appointment time |
| duration_minutes | Integer | Yes | Expected duration |
| type | Enum | Yes | CONSULTATION, FOLLOW_UP, PROCEDURE |
| status | Enum | Yes | SCHEDULED, WAITING, IN_PROGRESS, COMPLETED, CANCELLED, NO_SHOW |
| notes | Text | No | Appointment notes |
| cancellation_reason | Text | No | Reason if cancelled |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Last update |
| created_by | UUID | Yes | FK to User |

---

### Visit

Represents a clinical encounter/consultation.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| visit_number | String(20) | Yes | Unique visit ID (e.g., VIS-0001) |
| patient_id | UUID | Yes | FK to Patient |
| appointment_id | UUID | No | FK to Appointment |
| user_id | UUID | Yes | FK to User (treating dentist) |
| visit_date | DateTime | Yes | Visit date/time |
| chief_complaint | Text | No | Patient's main complaint |
| history | Text | No | History of present illness |
| clinical_findings | Text | No | Examination findings |
| diagnosis | Text | No | Diagnosis |
| advice | Text | No | Advice given |
| notes | Text | No | Additional notes |
| follow_up_date | Date | No | Recommended follow-up |
| status | Enum | Yes | IN_PROGRESS, COMPLETED |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Last update |

---

### DentalChart

Represents tooth-level status for a patient.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| patient_id | UUID | Yes | FK to Patient |
| tooth_number | Integer | Yes | Tooth number (1-32 adult, 51-85 child) |
| status | Enum | Yes | HEALTHY, CARIES, MISSING, RCT, CROWN, IMPLANT, EXTRACTION_PLANNED |
| notes | Text | No | Tooth-specific notes |
| updated_at | DateTime | Yes | Last update |
| updated_by | UUID | Yes | FK to User |

**Constraint:** Unique (patient_id, tooth_number)

---

### Prescription

Represents a prescription issued during a visit.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| rx_number | String(20) | Yes | Unique prescription number (e.g., RX-0001) |
| patient_id | UUID | Yes | FK to Patient |
| visit_id | UUID | Yes | FK to Visit |
| user_id | UUID | Yes | FK to User (prescribing doctor) |
| notes | Text | No | General instructions |
| created_at | DateTime | Yes | Creation timestamp |

---

### PrescriptionMedicine

Represents a medicine in a prescription.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| prescription_id | UUID | Yes | FK to Prescription |
| medicine_name | String(200) | Yes | Medicine name |
| dosage | String(100) | No | Dosage (e.g., 500mg) |
| frequency | String(100) | No | Frequency (e.g., 1-0-1) |
| duration | String(100) | No | Duration (e.g., 5 days) |
| instructions | Text | No | Special instructions |
| sequence | Integer | Yes | Order in prescription |

---

### TreatmentPlan

Represents a treatment plan for a patient.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| plan_number | String(20) | Yes | Unique plan number (e.g., TP-0001) |
| patient_id | UUID | Yes | FK to Patient |
| visit_id | UUID | No | FK to Visit (if created during visit) |
| created_by | UUID | Yes | FK to User |
| status | Enum | Yes | PROPOSED, APPROVED, IN_PROGRESS, COMPLETED, CANCELLED |
| total_cost | Decimal | Yes | Sum of procedure costs |
| notes | Text | No | Plan notes |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Last update |

---

### TreatmentProcedure

Represents a procedure in a treatment plan.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| treatment_plan_id | UUID | Yes | FK to TreatmentPlan |
| procedure_name | String(200) | Yes | Procedure name |
| tooth_number | Integer | No | Tooth number if applicable |
| cost | Decimal | Yes | Procedure cost |
| sessions | Integer | Yes | Number of sessions |
| status | Enum | Yes | PROPOSED, APPROVED, IN_PROGRESS, COMPLETED, CANCELLED |
| notes | Text | No | Procedure notes |
| sequence | Integer | Yes | Order in plan |
| completed_at | DateTime | No | Completion timestamp |

---

### Invoice

Represents a billing invoice.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| invoice_number | String(20) | Yes | Unique invoice number (e.g., INV-0001) |
| patient_id | UUID | Yes | FK to Patient |
| treatment_plan_id | UUID | No | FK to TreatmentPlan |
| created_by | UUID | Yes | FK to User |
| invoice_date | Date | Yes | Invoice date |
| subtotal | Decimal | Yes | Sum of items |
| discount | Decimal | Yes | Discount amount |
| tax | Decimal | Yes | Tax amount |
| total | Decimal | Yes | Final total |
| amount_paid | Decimal | Yes | Total paid |
| balance | Decimal | Yes | Outstanding balance |
| status | Enum | Yes | DRAFT, ISSUED, PARTIALLY_PAID, PAID, CANCELLED |
| notes | Text | No | Invoice notes |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Last update |

---

### InvoiceItem

Represents a line item in an invoice.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| invoice_id | UUID | Yes | FK to Invoice |
| procedure_id | UUID | No | FK to TreatmentProcedure |
| description | String(200) | Yes | Item description |
| quantity | Integer | Yes | Quantity |
| unit_price | Decimal | Yes | Price per unit |
| amount | Decimal | Yes | Total (qty * price) |
| sequence | Integer | Yes | Order in invoice |

---

### Payment

Represents a payment against an invoice.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| receipt_number | String(20) | Yes | Unique receipt number (e.g., RCP-0001) |
| invoice_id | UUID | Yes | FK to Invoice |
| amount | Decimal | Yes | Payment amount |
| payment_mode | Enum | Yes | CASH, UPI, CARD, BANK_TRANSFER |
| payment_date | Date | Yes | Payment date |
| reference | String(100) | No | Transaction reference |
| notes | Text | No | Payment notes |
| created_by | UUID | Yes | FK to User |
| created_at | DateTime | Yes | Creation timestamp |

---

### Document

Represents an uploaded document.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| patient_id | UUID | Yes | FK to Patient |
| visit_id | UUID | No | FK to Visit |
| document_type | Enum | Yes | XRAY, PHOTO, CONSENT, REPORT, OTHER |
| file_name | String(255) | Yes | Original file name |
| file_path | String(500) | Yes | Storage path |
| file_size | Integer | Yes | Size in bytes |
| mime_type | String(100) | Yes | MIME type |
| description | Text | No | Description |
| uploaded_by | UUID | Yes | FK to User |
| uploaded_at | DateTime | Yes | Upload timestamp |

---

### AuditLog

Represents an audit trail entry.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| user_id | UUID | Yes | FK to User |
| action | String(50) | Yes | Action performed |
| entity_type | String(50) | Yes | Entity type (Patient, Invoice, etc.) |
| entity_id | UUID | Yes | Entity ID |
| changes | JSON | No | Before/after values |
| ip_address | String(50) | No | Client IP |
| created_at | DateTime | Yes | Timestamp |

---

### ClinicSettings

Represents clinic configuration.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| clinic_name | String(200) | Yes | Clinic name |
| address | Text | No | Clinic address |
| phone | String(15) | No | Clinic phone |
| email | String(100) | No | Clinic email |
| logo_path | String(500) | No | Logo file path |
| prescription_header | Text | No | Prescription header text |
| invoice_header | Text | No | Invoice header text |
| working_hours | JSON | No | Working hours config |
| backup_schedule | JSON | No | Backup schedule config |
| updated_at | DateTime | Yes | Last update |

---

## Enumerations

### UserRole
- RECEPTIONIST
- DENTIST
- ADMIN

### Gender
- MALE
- FEMALE
- OTHER

### AppointmentType
- CONSULTATION
- FOLLOW_UP
- PROCEDURE

### AppointmentStatus
- SCHEDULED
- WAITING
- IN_PROGRESS
- COMPLETED
- CANCELLED
- NO_SHOW

### VisitStatus
- IN_PROGRESS
- COMPLETED

### ToothStatus
- HEALTHY
- CARIES
- MISSING
- RCT
- CROWN
- IMPLANT
- EXTRACTION_PLANNED

### TreatmentStatus
- PROPOSED
- APPROVED
- IN_PROGRESS
- COMPLETED
- CANCELLED

### InvoiceStatus
- DRAFT
- ISSUED
- PARTIALLY_PAID
- PAID
- CANCELLED

### PaymentMode
- CASH
- UPI
- CARD
- BANK_TRANSFER

### DocumentType
- XRAY
- PHOTO
- CONSENT
- REPORT
- OTHER

---

## Relationships Summary

| Parent | Child | Relationship | Description |
|--------|-------|--------------|-------------|
| Patient | Appointment | 1:N | Patient has many appointments |
| Patient | Visit | 1:N | Patient has many visits |
| Patient | DentalChart | 1:N | Patient has many tooth records |
| Patient | Prescription | 1:N | Patient has many prescriptions |
| Patient | TreatmentPlan | 1:N | Patient has many treatment plans |
| Patient | Invoice | 1:N | Patient has many invoices |
| Patient | Document | 1:N | Patient has many documents |
| Visit | Prescription | 1:N | Visit can have multiple prescriptions |
| Visit | TreatmentPlan | 1:N | Visit can create treatment plans |
| Prescription | PrescriptionMedicine | 1:N | Prescription has many medicines |
| TreatmentPlan | TreatmentProcedure | 1:N | Plan has many procedures |
| Invoice | InvoiceItem | 1:N | Invoice has many items |
| Invoice | Payment | 1:N | Invoice has many payments |
| User | * | 1:N | User creates/updates many records |

---

## Related Documents

- [Database Schema](database-schema.md)
- [API Specification](api-spec.md)
- [Architecture Overview](overview.md)
