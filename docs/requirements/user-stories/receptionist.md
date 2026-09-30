# User Stories: Receptionist

---

## Overview

The Receptionist is the front desk staff responsible for patient registration, appointment management, and billing operations.

---

## Patient Management

### US-R-001: Register New Patient

**As a** Receptionist  
**I want to** register a new patient with their details  
**So that** they can be tracked in the system for future visits

**Acceptance Criteria:**
- [ ] Can enter patient name (required)
- [ ] Can enter mobile number (required)
- [ ] Can enter gender (required)
- [ ] Can enter DOB or age
- [ ] Can enter address, email, emergency contact
- [ ] Can enter allergies, medical conditions, current medications
- [ ] System generates unique patient number (PAT-XXXXXX)
- [ ] Patient appears in search results after creation

**Priority:** P0 (MVP)

---

### US-R-002: Search Patient

**As a** Receptionist  
**I want to** search for a patient by name, mobile, or patient number  
**So that** I can quickly find their record

**Acceptance Criteria:**
- [ ] Can search by patient name (partial match)
- [ ] Can search by mobile number (partial match)
- [ ] Can search by patient number (exact match)
- [ ] Results display within 3 seconds
- [ ] Results show name, mobile, patient number, last visit date
- [ ] Can click result to open patient profile

**Priority:** P0 (MVP)

---

### US-R-003: Update Patient Information

**As a** Receptionist  
**I want to** update a patient's contact information  
**So that** their records stay current

**Acceptance Criteria:**
- [ ] Can edit all patient fields except patient number
- [ ] Changes are saved immediately
- [ ] Audit log captures the change
- [ ] Cannot delete patient (only Admin)

**Priority:** P0 (MVP)

---

### US-R-004: View Patient Profile

**As a** Receptionist  
**I want to** view a patient's profile and history  
**So that** I can assist them with inquiries

**Acceptance Criteria:**
- [ ] Can see patient details
- [ ] Can see appointment history
- [ ] Can see billing history and outstanding balance
- [ ] Cannot see clinical notes (restricted to Dentist)

**Priority:** P0 (MVP)

---

## Appointment Management

### US-R-005: Book Appointment

**As a** Receptionist  
**I want to** book an appointment for a patient  
**So that** they have a scheduled time to visit

**Acceptance Criteria:**
- [ ] Can select patient
- [ ] Can select date and time
- [ ] Can select dentist (optional)
- [ ] Can select appointment type (Consultation, Follow-up, Procedure)
- [ ] Can add notes
- [ ] System prevents double-booking same slot
- [ ] Appointment appears in calendar

**Priority:** P0 (MVP)

---

### US-R-006: View Today's Appointments

**As a** Receptionist  
**I want to** see all appointments for today  
**So that** I can manage the queue

**Acceptance Criteria:**
- [ ] Can see list of today's appointments
- [ ] Shows patient name, time, type, status
- [ ] Shows dentist assigned
- [ ] Can filter by dentist
- [ ] Can sort by time

**Priority:** P0 (MVP)

---

### US-R-007: Mark Patient as Waiting

**As a** Receptionist  
**I want to** mark a patient as "Waiting" when they arrive  
**So that** the dentist knows they are ready

**Acceptance Criteria:**
- [ ] Can change appointment status to "Waiting"
- [ ] Waiting patients appear in queue view
- [ ] Timestamp recorded for arrival

**Priority:** P0 (MVP)

---

### US-R-008: Reschedule Appointment

**As a** Receptionist  
**I want to** reschedule an appointment to a different date/time  
**So that** patients can change their plans

**Acceptance Criteria:**
- [ ] Can change date and time
- [ ] Original slot becomes available
- [ ] New slot is blocked
- [ ] History shows rescheduling

**Priority:** P0 (MVP)

---

### US-R-009: Cancel Appointment

**As a** Receptionist  
**I want to** cancel an appointment  
**So that** the slot becomes available for others

**Acceptance Criteria:**
- [ ] Can cancel appointment
- [ ] Must enter cancellation reason
- [ ] Slot becomes available
- [ ] Cancelled appointment retained in history

**Priority:** P0 (MVP)

---

### US-R-010: Create Walk-in Appointment

**As a** Receptionist  
**I want to** create a walk-in appointment for a patient without prior booking  
**So that** they can be seen today

**Acceptance Criteria:**
- [ ] Can create appointment for current date
- [ ] Marked as walk-in type
- [ ] Added to today's queue

**Priority:** P0 (MVP)

---

## Billing

### US-R-011: Create Invoice

**As a** Receptionist  
**I want to** create an invoice for a patient  
**So that** they can pay for services

**Acceptance Criteria:**
- [ ] Can select patient
- [ ] Can add line items with description and amount
- [ ] Can apply discount (amount or percentage)
- [ ] System calculates total
- [ ] Can save as draft or issue immediately

**Priority:** P0 (MVP)

---

### US-R-012: Create Invoice from Treatment Plan

**As a** Receptionist  
**I want to** generate an invoice from an approved treatment plan  
**So that** I don't have to re-enter procedure details

**Acceptance Criteria:**
- [ ] Can select treatment plan
- [ ] Procedures auto-populate as line items
- [ ] Costs from treatment plan used
- [ ] Can modify before issuing

**Priority:** P0 (MVP)

---

### US-R-013: Collect Payment

**As a** Receptionist  
**I want to** record a payment against an invoice  
**So that** the patient's balance is updated

**Acceptance Criteria:**
- [ ] Can select invoice
- [ ] Can enter payment amount
- [ ] Can select payment mode (Cash, UPI, Card, Bank Transfer)
- [ ] Can enter reference number for non-cash
- [ ] System updates invoice balance
- [ ] Receipt generated automatically

**Priority:** P0 (MVP)

---

### US-R-014: Print Receipt

**As a** Receptionist  
**I want to** print a receipt for the patient  
**So that** they have proof of payment

**Acceptance Criteria:**
- [ ] Can print receipt after payment
- [ ] Receipt shows payment details
- [ ] Receipt shows remaining balance (if any)
- [ ] Can reprint previous receipts

**Priority:** P0 (MVP)

---

### US-R-015: View Outstanding Balance

**As a** Receptionist  
**I want to** see a patient's outstanding balance  
**So that** I can collect pending payments

**Acceptance Criteria:**
- [ ] Outstanding balance visible on patient profile
- [ ] Can see list of unpaid/partially paid invoices
- [ ] Can collect payment from this view

**Priority:** P0 (MVP)

---

## Documents

### US-R-016: Upload Document

**As a** Receptionist  
**I want to** upload documents for a patient  
**So that** external reports can be stored

**Acceptance Criteria:**
- [ ] Can upload images (JPG, PNG)
- [ ] Can upload PDFs
- [ ] Can select document type (X-ray, Photo, Consent, Report, Other)
- [ ] Can add description
- [ ] Document linked to patient

**Priority:** P0 (MVP)

---

### US-R-017: View Patient Documents

**As a** Receptionist  
**I want to** view documents uploaded for a patient  
**So that** I can assist with inquiries

**Acceptance Criteria:**
- [ ] Can see list of documents
- [ ] Can view/download documents
- [ ] Cannot delete documents (Admin only)

**Priority:** P0 (MVP)

---

## Reports

### US-R-018: View Daily Collections

**As a** Receptionist  
**I want to** see today's collection summary  
**So that** I can reconcile at end of day

**Acceptance Criteria:**
- [ ] Shows total collected today
- [ ] Breakdown by payment mode
- [ ] List of individual payments
- [ ] Can filter by date range

**Priority:** P0 (MVP)

---

## Related Documents

- [Dentist User Stories](dentist.md)
- [Admin User Stories](admin.md)
- [PRD](../prd.md)
