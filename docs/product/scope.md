# DentOS Product Scope

---

## MVP Scope

### In Scope (MVP)

#### Patient Registry

**Capabilities:**
- Create Patient
- Update Patient
- Search Patient
- Patient Timeline
- Medical Alerts

**Patient Data:**
- Name
- Mobile
- DOB / Age
- Gender
- Address
- Email
- Emergency Contact
- Allergies
- Medical Conditions
- Current Medications

---

#### Appointment Management

**Capabilities:**
- Book Appointment
- Reschedule Appointment
- Cancel Appointment
- Queue Management
- Follow-Up Scheduling

---

#### Clinical Encounters

**Each Visit Stores:**
- Chief Complaint
- History
- Clinical Findings
- Diagnosis
- Notes
- Advice
- Follow-Up

---

#### Dental Chart

Simple tooth-level chart.

**Tooth Status Options:**
- Healthy
- Caries
- Missing
- RCT
- Crown
- Implant
- Extraction Planned

> Note: Advanced periodontal charting is intentionally excluded from MVP.

---

#### Prescription Module

**Generate:**
- Prescription Number
- Patient Details
- Medicines
- Instructions
- Doctor Details

**Output:**
- Print
- PDF
- History

---

#### Treatment Plan

**Capture:**
- Procedure
- Tooth
- Cost
- Sessions
- Notes

**Status:**
- Proposed
- Approved
- In Progress
- Completed
- Cancelled

---

#### Billing

**Generate:**
- Invoice
- Payment
- Receipt

**Supported Payment Modes:**
- Cash
- UPI
- Card
- Bank Transfer

**Support:**
- Outstanding Balance
- Partial Payment
- Multiple Payments

---

#### Document Storage

**Store:**
- X-Rays
- Patient Photos
- Consent Forms
- Invoices
- Receipts
- Prescriptions

---

#### Reports

- Daily Collections
- Outstanding Payments
- Upcoming Follow-Ups
- Patient Statistics

---

## Out of Scope (Deferred)

Explicitly deferred to future phases:

| Feature | Reason for Deferral |
|---------|---------------------|
| Inventory Management | Adds complexity, not core to patient care |
| Lab Management | Requires external integrations |
| Payroll | HR system, not clinic operations |
| Insurance Claims | Requires payer integrations |
| Online Consultations | Telemedicine is different product |
| Patient Portal | Requires public-facing infrastructure |
| AI Diagnosis | Research-level feature |
| Marketing CRM | Sales tool, not operations |
| Multi-Branch Support | Scale feature for Phase 4 |
| Mobile Applications | Web-first approach for MVP |

---

## Scope Boundaries

### DentOS Will

- Manage patient records end-to-end
- Handle all billing and payments
- Store clinical documents
- Work offline
- Backup data automatically

### DentOS Will Not

- Replace specialized imaging software
- Handle insurance claim submissions
- Manage inventory or supplies
- Process payroll
- Provide telemedicine capabilities

---

## Related Documents

- [Product Vision](vision.md)
- [Goals & Success Criteria](goals.md)
- [Product Roadmap](roadmap.md)
- [Product Requirements](../requirements/prd.md)
