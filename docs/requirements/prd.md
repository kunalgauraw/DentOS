# DentOS Product Requirements Document (PRD)

---

## Document Info

| Field | Value |
|-------|-------|
| Version | 0.1 (Draft) |
| Status | In Progress |
| Last Updated | TBD |

---

## Overview

This document details the functional requirements for DentOS MVP. For product vision and scope, see [Product Vision](../product/vision.md) and [Product Scope](../product/scope.md).

---

## User Roles

| Role | Description | Key Responsibilities |
|------|-------------|---------------------|
| **Receptionist** | Front desk staff | Patient registration, appointments, billing |
| **Dentist** | Clinical staff | Consultations, diagnosis, prescriptions, treatment |
| **Admin** | Clinic owner/manager | User management, reports, settings, backups |

---

## Functional Requirements

### FR-1: Patient Registry

#### FR-1.1: Create Patient
- System shall allow creating new patient record
- Required fields: Name, Mobile, Gender
- Optional fields: DOB/Age, Address, Email, Emergency Contact
- System shall generate unique Patient ID

#### FR-1.2: Update Patient
- System shall allow updating patient information
- System shall maintain audit trail of changes

#### FR-1.3: Search Patient
- System shall support search by: Name, Mobile, Patient ID
- Search shall return results within 3 seconds
- Search shall support partial matching

#### FR-1.4: Patient Timeline
- System shall display chronological history of all patient interactions
- Timeline shall include: Visits, Prescriptions, Invoices, Documents

#### FR-1.5: Medical Alerts
- System shall store and display: Allergies, Medical Conditions, Current Medications
- Alerts shall be prominently visible during consultations

---

### FR-2: Appointment Management

#### FR-2.1: Book Appointment
- System shall allow booking appointments for specific date/time
- System shall prevent double-booking same slot

#### FR-2.2: Reschedule Appointment
- System shall allow changing appointment date/time
- System shall maintain history of changes

#### FR-2.3: Cancel Appointment
- System shall allow cancellation with reason
- Cancelled appointments shall remain in history

#### FR-2.4: Queue Management
- System shall display today's appointments
- System shall show patient status: Waiting, In Consultation, Completed

#### FR-2.5: Follow-Up Scheduling
- System shall allow scheduling follow-up from consultation screen
- System shall link follow-up to original visit

---

### FR-3: Clinical Encounters

#### FR-3.1: Create Visit
- System shall create visit record when patient consultation begins
- Visit shall be linked to patient and appointment (if applicable)

#### FR-3.2: Record Clinical Data
- System shall capture: Chief Complaint, History, Clinical Findings, Diagnosis, Notes, Advice, Follow-Up
- All fields shall be free-text with optional templates

#### FR-3.3: Dental Chart
- System shall display visual tooth chart (adult: 32 teeth, child: 20 teeth)
- Each tooth shall have status: Healthy, Caries, Missing, RCT, Crown, Implant, Extraction Planned
- Chart shall persist across visits

---

### FR-4: Prescription Module

#### FR-4.1: Create Prescription
- System shall generate prescription linked to visit
- Prescription shall include: Medicines, Dosage, Duration, Instructions

#### FR-4.2: Medicine Entry
- System shall allow adding multiple medicines
- System shall support free-text entry (no master required for MVP)

#### FR-4.3: Print/Export Prescription
- System shall generate printable prescription
- System shall generate PDF version
- Prescription shall include: Clinic header, Patient details, Doctor details, Date

---

### FR-5: Treatment Plan

#### FR-5.1: Create Treatment Plan
- System shall allow creating treatment plan with multiple procedures
- Each procedure shall have: Name, Tooth (optional), Cost, Sessions, Notes

#### FR-5.2: Treatment Status
- System shall track status: Proposed, Approved, In Progress, Completed, Cancelled
- Status changes shall be logged

#### FR-5.3: Link to Billing
- Approved treatments shall be available for invoicing

---

### FR-6: Billing

#### FR-6.1: Create Invoice
- System shall generate invoice from treatment plan or ad-hoc items
- Invoice shall include: Line items, Amounts, Taxes (if applicable), Total

#### FR-6.2: Record Payment
- System shall record payments against invoice
- Supported modes: Cash, UPI, Card, Bank Transfer
- System shall support partial payments

#### FR-6.3: Generate Receipt
- System shall generate receipt for each payment
- Receipt shall be printable and exportable as PDF

#### FR-6.4: Outstanding Balance
- System shall track outstanding balance per patient
- System shall display outstanding in patient profile

---

### FR-7: Document Storage

#### FR-7.1: Upload Documents
- System shall allow uploading: Images, PDFs
- Documents shall be linked to patient
- Supported types: X-Rays, Photos, Consent Forms, External Reports

#### FR-7.2: View Documents
- System shall display documents in patient timeline
- Images shall be viewable inline

---

### FR-8: Reports

#### FR-8.1: Daily Collections
- System shall generate daily collection report
- Report shall show: Total collected, Payment mode breakdown

#### FR-8.2: Outstanding Payments
- System shall list patients with outstanding balances

#### FR-8.3: Upcoming Follow-Ups
- System shall list scheduled follow-ups

#### FR-8.4: Patient Statistics
- System shall show: Total patients, New patients (period), Visit count

---

### FR-9: User Management

#### FR-9.1: User Authentication
- System shall require login with username/password
- System shall support automatic logout after inactivity

#### FR-9.2: Role-Based Access
- System shall enforce permissions based on role
- Receptionist: Patients, Appointments, Billing
- Dentist: All clinical features
- Admin: All features + User management + Settings

---

### FR-10: Backup

#### FR-10.1: Automated Backup
- System shall perform daily automated backup
- Backup shall include: Database, Documents, Configuration

#### FR-10.2: Backup Destination
- System shall support backup to: Local folder, OneDrive, Google Drive

#### FR-10.3: Backup Encryption
- Backups shall be encrypted before upload

---

## Non-Functional Requirements

### NFR-1: Performance
- Page load time: < 2 seconds
- Search results: < 3 seconds
- Report generation: < 10 seconds

### NFR-2: Availability
- System shall operate without internet connection
- System shall be available during clinic hours (99.9% uptime)

### NFR-3: Security
- All passwords shall be hashed
- Audit trail for sensitive operations
- Session timeout after 15 minutes of inactivity

### NFR-4: Usability
- System shall be usable on 1366x768 resolution minimum
- System shall work on Chrome, Edge browsers

---

## Related Documents

- [Product Scope](../product/scope.md)
- [User Stories](user-stories/)
- [Business Rules](business-rules.md)
- [Architecture Overview](../architecture/overview.md)
