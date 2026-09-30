# DentOS Business Rules

---

## Overview

This document defines the business rules, validations, calculations, and constraints for DentOS.

---

## Patient Management

### PAT: Patient Rules

| ID | Rule | Description |
|----|------|-------------|
| PAT-001 | Patient Number Format | Auto-generated as PAT-XXXXXX (6-digit sequential) |
| PAT-002 | Required Fields | Name, Mobile, Gender are mandatory |
| PAT-003 | Mobile Format | 10-digit number, must be numeric |
| PAT-004 | Mobile Uniqueness | Warning if mobile already exists (not blocked) |
| PAT-005 | Age Calculation | If DOB provided, age calculated automatically |
| PAT-006 | Age or DOB | Either DOB or Age must be provided |
| PAT-007 | Patient Deletion | Patients cannot be deleted, only deactivated |
| PAT-008 | Deactivation | Only Admin can deactivate patients |
| PAT-009 | Reactivation | Deactivated patients can be reactivated by Admin |
| PAT-010 | Search Minimum | Search requires at least 2 characters |

---

## Appointment Management

### APT: Appointment Rules

| ID | Rule | Description |
|----|------|-------------|
| APT-001 | No Double Booking | Same dentist cannot have overlapping appointments |
| APT-002 | Future Dates Only | Appointments can only be booked for today or future |
| APT-003 | Working Hours | Appointments only during configured working hours |
| APT-004 | Minimum Duration | Minimum appointment duration: 15 minutes |
| APT-005 | Default Duration | Default duration: 30 minutes |
| APT-006 | Cancellation Reason | Cancellation requires a reason |
| APT-007 | Status Flow | SCHEDULED → WAITING → IN_PROGRESS → COMPLETED |
| APT-008 | No-Show Marking | Only Admin/Receptionist can mark as NO_SHOW |
| APT-009 | Past Appointments | Past appointments cannot be modified |
| APT-010 | Walk-in Type | Walk-in appointments auto-set to current date/time |

### Appointment Status Transitions

```
SCHEDULED → WAITING       (Patient arrives)
SCHEDULED → CANCELLED     (Cancelled before arrival)
SCHEDULED → NO_SHOW       (Patient didn't arrive)
WAITING   → IN_PROGRESS   (Consultation starts)
WAITING   → CANCELLED     (Cancelled after arrival)
IN_PROGRESS → COMPLETED   (Consultation ends)
```

---

## Clinical Encounters

### VIS: Visit Rules

| ID | Rule | Description |
|----|------|-------------|
| VIS-001 | Visit Number Format | Auto-generated as VIS-XXXXXX (6-digit sequential) |
| VIS-002 | One Active Visit | Patient can have only one IN_PROGRESS visit at a time |
| VIS-003 | Visit Creation | Visit created when consultation starts |
| VIS-004 | Dentist Required | Visit must be associated with a dentist |
| VIS-005 | Completion | Visit marked complete when dentist finishes |
| VIS-006 | Edit Window | Completed visits can be edited within 24 hours |
| VIS-007 | After Edit Window | After 24 hours, only Admin can edit with audit log |

### CHT: Dental Chart Rules

| ID | Rule | Description |
|----|------|-------------|
| CHT-001 | Adult Teeth | Teeth numbered 1-32 for adults |
| CHT-002 | Child Teeth | Teeth numbered 51-55, 61-65, 71-75, 81-85 for children |
| CHT-003 | Status Options | HEALTHY, CARIES, MISSING, RCT, CROWN, IMPLANT, EXTRACTION_PLANNED |
| CHT-004 | Default Status | New teeth default to HEALTHY |
| CHT-005 | History Retention | Previous status retained in history |
| CHT-006 | Update Logging | All changes logged with user and timestamp |

---

## Prescription

### RX: Prescription Rules

| ID | Rule | Description |
|----|------|-------------|
| RX-001 | Rx Number Format | Auto-generated as RX-XXXXXX (6-digit sequential) |
| RX-002 | Visit Required | Prescription must be linked to a visit |
| RX-003 | Minimum Medicines | At least one medicine required |
| RX-004 | Medicine Name Required | Medicine name is mandatory |
| RX-005 | Prescriber Capture | Prescribing doctor auto-captured from session |
| RX-006 | Immutable | Prescriptions cannot be edited after creation |
| RX-007 | Reprint Allowed | Previous prescriptions can be reprinted |
| RX-008 | Allergy Warning | Show warning if patient has allergies |

---

## Treatment Plan

### TRT: Treatment Plan Rules

| ID | Rule | Description |
|----|------|-------------|
| TRT-001 | Plan Number Format | Auto-generated as TP-XXXXXX (6-digit sequential) |
| TRT-002 | Minimum Procedures | At least one procedure required |
| TRT-003 | Cost Required | Procedure cost must be >= 0 |
| TRT-004 | Sessions Default | Default sessions: 1 |
| TRT-005 | Total Calculation | Total = Sum of all procedure costs |
| TRT-006 | Status Flow | PROPOSED → APPROVED → IN_PROGRESS → COMPLETED |
| TRT-007 | Approval | Patient approval required before IN_PROGRESS |
| TRT-008 | Procedure Status | Individual procedures track their own status |
| TRT-009 | Completion | Plan COMPLETED when all procedures COMPLETED |
| TRT-010 | Cancellation | Plan can be cancelled at any stage except COMPLETED |

### Treatment Status Transitions

```
PROPOSED → APPROVED       (Patient agrees)
PROPOSED → CANCELLED      (Patient declines)
APPROVED → IN_PROGRESS    (Treatment starts)
APPROVED → CANCELLED      (Changed mind)
IN_PROGRESS → COMPLETED   (All procedures done)
IN_PROGRESS → CANCELLED   (Treatment stopped)
```

---

## Billing

### INV: Invoice Rules

| ID | Rule | Description |
|----|------|-------------|
| INV-001 | Invoice Number Format | Auto-generated as INV-XXXXXX (6-digit sequential) |
| INV-002 | Minimum Items | At least one line item required |
| INV-003 | Item Amount | Line item amount must be > 0 |
| INV-004 | Discount Limit | Discount cannot exceed subtotal |
| INV-005 | Total Calculation | Total = Subtotal - Discount + Tax |
| INV-006 | Balance Calculation | Balance = Total - Amount Paid |
| INV-007 | Draft Editable | Draft invoices can be edited |
| INV-008 | Issued Immutable | Issued invoices cannot be edited |
| INV-009 | Cancellation | Only Admin can cancel invoices |
| INV-010 | Paid No Cancel | Fully paid invoices cannot be cancelled |
| INV-011 | Status Auto-Update | Status auto-updates based on payments |

### Invoice Status Rules

| Condition | Status |
|-----------|--------|
| Not yet issued | DRAFT |
| Issued, no payment | ISSUED |
| Partial payment received | PARTIALLY_PAID |
| Full payment received | PAID |
| Cancelled by Admin | CANCELLED |

### Invoice Calculations

```
Subtotal = SUM(item.quantity * item.unit_price)
Discount = Manual entry (amount or percentage of subtotal)
Tax = Subtotal * Tax Rate (if applicable)
Total = Subtotal - Discount + Tax
Balance = Total - Amount Paid
```

---

## Payment

### PAY: Payment Rules

| ID | Rule | Description |
|----|------|-------------|
| PAY-001 | Receipt Number Format | Auto-generated as RCP-XXXXXX (6-digit sequential) |
| PAY-002 | Amount Positive | Payment amount must be > 0 |
| PAY-003 | Amount Limit | Payment amount cannot exceed invoice balance |
| PAY-004 | Mode Required | Payment mode is mandatory |
| PAY-005 | Reference for Non-Cash | Reference number required for UPI, Card, Bank Transfer |
| PAY-006 | Auto Receipt | Receipt generated automatically on payment |
| PAY-007 | Invoice Update | Invoice balance updated immediately |
| PAY-008 | No Refunds | Refunds not supported in MVP (manual adjustment) |
| PAY-009 | Immutable | Payments cannot be edited or deleted |

### Payment Modes

| Mode | Reference Required | Description |
|------|-------------------|-------------|
| CASH | No | Cash payment |
| UPI | Yes | UPI transaction ID |
| CARD | Yes | Card transaction reference |
| BANK_TRANSFER | Yes | Bank reference number |

---

## Documents

### DOC: Document Rules

| ID | Rule | Description |
|----|------|-------------|
| DOC-001 | Allowed Types | JPG, PNG, PDF only |
| DOC-002 | Max Size | Maximum file size: 10 MB |
| DOC-003 | Patient Required | Document must be linked to patient |
| DOC-004 | Type Required | Document type must be specified |
| DOC-005 | Deletion | Only Admin can delete documents |
| DOC-006 | Storage Path | Files stored in PatientFiles/{PatientID}/ |
| DOC-007 | Name Sanitization | File names sanitized for storage |

---

## User & Authentication

### USR: User Rules

| ID | Rule | Description |
|----|------|-------------|
| USR-001 | Username Unique | Username must be unique |
| USR-002 | Username Format | Alphanumeric, 4-50 characters |
| USR-003 | Password Minimum | Minimum 8 characters |
| USR-004 | Password Complexity | At least 1 uppercase, 1 number |
| USR-005 | Role Required | User must have exactly one role |
| USR-006 | Admin Minimum | At least one Admin must exist |
| USR-007 | Self Deactivation | Users cannot deactivate themselves |
| USR-008 | Session Timeout | Auto-logout after 15 minutes inactivity |
| USR-009 | Token Expiry | JWT token expires after 8 hours |

### AUTH: Authentication Rules

| ID | Rule | Description |
|----|------|-------------|
| AUTH-001 | Login Required | All pages require authentication except login |
| AUTH-002 | Failed Attempts | Account locked after 5 failed attempts |
| AUTH-003 | Lockout Duration | Lockout for 15 minutes |
| AUTH-004 | Password Hash | Passwords stored as bcrypt hash |
| AUTH-005 | Audit Login | All login attempts logged |

---

## Audit

### AUD: Audit Rules

| ID | Rule | Description |
|----|------|-------------|
| AUD-001 | Immutable | Audit logs cannot be modified or deleted |
| AUD-002 | Retention | Audit logs retained for 7 years |
| AUD-003 | Required Fields | User, Action, Entity, Timestamp required |
| AUD-004 | Change Capture | Before/after values captured for updates |
| AUD-005 | IP Capture | Client IP address captured |

### Audited Actions

| Entity | Actions Audited |
|--------|-----------------|
| Patient | CREATE, UPDATE, DEACTIVATE |
| Visit | CREATE, UPDATE, COMPLETE |
| Prescription | CREATE, PRINT |
| Treatment Plan | CREATE, UPDATE, STATUS_CHANGE |
| Invoice | CREATE, ISSUE, CANCEL |
| Payment | CREATE |
| Document | UPLOAD, DELETE |
| User | CREATE, UPDATE, DEACTIVATE, LOGIN, LOGOUT, FAILED_LOGIN |
| Settings | UPDATE |

---

## Backup

### BAK: Backup Rules

| ID | Rule | Description |
|----|------|-------------|
| BAK-001 | Daily Backup | Automatic backup runs daily at configured time |
| BAK-002 | Contents | Backup includes database + documents + config |
| BAK-003 | Encryption | Backups encrypted with AES-256 |
| BAK-004 | Retention | Local backups retained for 7 days |
| BAK-005 | Cloud Retention | Cloud backups retained for 90 days |
| BAK-006 | Restore Warning | Restore requires confirmation (destructive) |
| BAK-007 | Restore Audit | Restore action logged |

---

## Number Sequences

| Entity | Prefix | Format | Example |
|--------|--------|--------|---------|
| Patient | PAT- | PAT-XXXXXX | PAT-000001 |
| Visit | VIS- | VIS-XXXXXX | VIS-000001 |
| Prescription | RX- | RX-XXXXXX | RX-000001 |
| Treatment Plan | TP- | TP-XXXXXX | TP-000001 |
| Invoice | INV- | INV-XXXXXX | INV-000001 |
| Receipt | RCP- | RCP-XXXXXX | RCP-000001 |

---

## Related Documents

- [PRD](prd.md)
- [User Stories](user-stories/)
- [Domain Model](../architecture/domain-model.md)
