# User Stories: Dentist

---

## Overview

The Dentist is the clinical staff responsible for patient consultations, diagnosis, treatment planning, and prescriptions.

---

## Queue & Appointments

### US-D-001: View Patient Queue

**As a** Dentist  
**I want to** see the list of patients waiting for me  
**So that** I can call the next patient

**Acceptance Criteria:**
- [ ] Can see patients with status "Waiting"
- [ ] Shows patient name, appointment time, type
- [ ] Shows waiting duration
- [ ] Sorted by arrival time
- [ ] Can filter by my appointments only

**Priority:** P0 (MVP)

---

### US-D-002: Start Consultation

**As a** Dentist  
**I want to** start a consultation for a waiting patient  
**So that** I can begin the clinical encounter

**Acceptance Criteria:**
- [ ] Can select patient from queue
- [ ] Appointment status changes to "In Progress"
- [ ] Visit record created automatically
- [ ] Visit linked to appointment

**Priority:** P0 (MVP)

---

## Patient Information

### US-D-003: View Patient History

**As a** Dentist  
**I want to** see a patient's complete history  
**So that** I can make informed clinical decisions

**Acceptance Criteria:**
- [ ] Can see all previous visits
- [ ] Can see all prescriptions
- [ ] Can see all treatment plans
- [ ] Can see dental chart history
- [ ] Can see uploaded documents (X-rays, etc.)

**Priority:** P0 (MVP)

---

### US-D-004: View Medical Alerts

**As a** Dentist  
**I want to** see a patient's allergies and medical conditions prominently  
**So that** I don't prescribe contraindicated medications

**Acceptance Criteria:**
- [ ] Allergies displayed prominently on consultation screen
- [ ] Medical conditions visible
- [ ] Current medications visible
- [ ] Alert shown if allergies exist

**Priority:** P0 (MVP)

---

## Clinical Encounter

### US-D-005: Record Chief Complaint

**As a** Dentist  
**I want to** record the patient's chief complaint  
**So that** the reason for visit is documented

**Acceptance Criteria:**
- [ ] Can enter free-text chief complaint
- [ ] Saved with visit record
- [ ] Visible in visit history

**Priority:** P0 (MVP)

---

### US-D-006: Record Clinical Findings

**As a** Dentist  
**I want to** record my clinical examination findings  
**So that** they are documented for future reference

**Acceptance Criteria:**
- [ ] Can enter history of present illness
- [ ] Can enter clinical findings
- [ ] Can enter diagnosis
- [ ] Can enter advice given
- [ ] All fields are free-text

**Priority:** P0 (MVP)

---

### US-D-007: Complete Visit

**As a** Dentist  
**I want to** mark a visit as complete  
**So that** the patient can proceed to billing

**Acceptance Criteria:**
- [ ] Can mark visit as "Completed"
- [ ] Appointment status changes to "Completed"
- [ ] Patient removed from active queue
- [ ] Visit timestamp recorded

**Priority:** P0 (MVP)

---

## Dental Chart

### US-D-008: View Dental Chart

**As a** Dentist  
**I want to** see the patient's dental chart  
**So that** I can see the status of each tooth

**Acceptance Criteria:**
- [ ] Visual chart showing all teeth (adult: 32, child: 20)
- [ ] Each tooth shows current status with color coding
- [ ] Can see tooth-specific notes
- [ ] Chart persists across visits

**Priority:** P0 (MVP)

---

### US-D-009: Update Tooth Status

**As a** Dentist  
**I want to** update the status of a tooth  
**So that** the chart reflects current condition

**Acceptance Criteria:**
- [ ] Can click on tooth to select
- [ ] Can set status: Healthy, Caries, Missing, RCT, Crown, Implant, Extraction Planned
- [ ] Can add notes for tooth
- [ ] Change logged with timestamp and user
- [ ] Previous status retained in history

**Priority:** P0 (MVP)

---

## Prescription

### US-D-010: Create Prescription

**As a** Dentist  
**I want to** create a prescription for the patient  
**So that** they can get the required medications

**Acceptance Criteria:**
- [ ] Can add multiple medicines
- [ ] For each medicine: name, dosage, frequency, duration, instructions
- [ ] Patient details auto-filled
- [ ] Prescription number generated
- [ ] Linked to current visit

**Priority:** P0 (MVP)

---

### US-D-011: Print Prescription

**As a** Dentist  
**I want to** print the prescription  
**So that** the patient can take it to the pharmacy

**Acceptance Criteria:**
- [ ] Prescription formatted for printing (A4/A5)
- [ ] Includes clinic header
- [ ] Includes patient details
- [ ] Includes my details and signature space
- [ ] Can print multiple copies

**Priority:** P0 (MVP)

---

### US-D-012: Save Prescription as PDF

**As a** Dentist  
**I want to** save the prescription as PDF  
**So that** it can be shared digitally or reprinted later

**Acceptance Criteria:**
- [ ] Can download prescription as PDF
- [ ] PDF stored with patient documents
- [ ] Can access from patient history

**Priority:** P0 (MVP)

---

### US-D-013: View Prescription History

**As a** Dentist  
**I want to** see previous prescriptions for a patient  
**So that** I can review what was prescribed before

**Acceptance Criteria:**
- [ ] List of all prescriptions for patient
- [ ] Can view details of each prescription
- [ ] Can reprint previous prescriptions

**Priority:** P0 (MVP)

---

## Treatment Plan

### US-D-014: Create Treatment Plan

**As a** Dentist  
**I want to** create a treatment plan for the patient  
**So that** they understand the proposed procedures and costs

**Acceptance Criteria:**
- [ ] Can add multiple procedures
- [ ] For each procedure: name, tooth (optional), cost, sessions, notes
- [ ] System calculates total cost
- [ ] Plan linked to patient
- [ ] Plan number generated

**Priority:** P0 (MVP)

---

### US-D-015: Update Treatment Plan Status

**As a** Dentist  
**I want to** update the status of a treatment plan  
**So that** progress is tracked

**Acceptance Criteria:**
- [ ] Can change plan status: Proposed → Approved → In Progress → Completed
- [ ] Can update individual procedure status
- [ ] Can mark procedure as completed with date
- [ ] Status changes logged

**Priority:** P0 (MVP)

---

### US-D-016: View Treatment History

**As a** Dentist  
**I want to** see all treatment plans for a patient  
**So that** I can review past and ongoing treatments

**Acceptance Criteria:**
- [ ] List of all treatment plans
- [ ] Shows status of each plan
- [ ] Can view procedure details
- [ ] Can see completed vs pending procedures

**Priority:** P0 (MVP)

---

## Documents

### US-D-017: Upload Clinical Documents

**As a** Dentist  
**I want to** upload X-rays and clinical photos  
**So that** they are stored with the patient record

**Acceptance Criteria:**
- [ ] Can upload images during consultation
- [ ] Can categorize as X-ray, Photo, etc.
- [ ] Can link to current visit
- [ ] Can add description

**Priority:** P0 (MVP)

---

### US-D-018: View Patient Documents

**As a** Dentist  
**I want to** view all documents for a patient  
**So that** I can review X-rays and reports

**Acceptance Criteria:**
- [ ] Can see all documents
- [ ] Can view images inline
- [ ] Can download documents
- [ ] Can filter by type

**Priority:** P0 (MVP)

---

## Follow-up

### US-D-019: Schedule Follow-up

**As a** Dentist  
**I want to** schedule a follow-up appointment  
**So that** the patient returns for continued care

**Acceptance Criteria:**
- [ ] Can set follow-up date from consultation screen
- [ ] Appointment created automatically
- [ ] Linked to current visit
- [ ] Marked as "Follow-up" type

**Priority:** P1 (Should Have)

---

### US-D-020: View Upcoming Follow-ups

**As a** Dentist  
**I want to** see patients due for follow-up  
**So that** I can ensure continuity of care

**Acceptance Criteria:**
- [ ] List of upcoming follow-ups
- [ ] Shows patient name, date, original visit reason
- [ ] Can filter by date range

**Priority:** P1 (Should Have)

---

## Related Documents

- [Receptionist User Stories](receptionist.md)
- [Admin User Stories](admin.md)
- [PRD](../prd.md)
