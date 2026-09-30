# User Stories: Admin

---

## Overview

The Admin is the clinic owner or manager responsible for system configuration, user management, reports, and backup operations. Admin has all permissions of Receptionist and Dentist, plus administrative functions.

---

## User Management

### US-A-001: Create User

**As an** Admin  
**I want to** create user accounts for staff  
**So that** they can access the system

**Acceptance Criteria:**
- [ ] Can enter username (unique)
- [ ] Can enter name, email, phone
- [ ] Can set initial password
- [ ] Can assign role (Receptionist, Dentist, Admin)
- [ ] User can login after creation

**Priority:** P0 (MVP)

---

### US-A-002: Edit User

**As an** Admin  
**I want to** edit user details  
**So that** I can update their information or role

**Acceptance Criteria:**
- [ ] Can edit name, email, phone
- [ ] Can change role
- [ ] Cannot change username
- [ ] Changes take effect immediately

**Priority:** P0 (MVP)

---

### US-A-003: Deactivate User

**As an** Admin  
**I want to** deactivate a user account  
**So that** they can no longer access the system

**Acceptance Criteria:**
- [ ] Can set user as inactive
- [ ] Inactive user cannot login
- [ ] User's historical records retained
- [ ] Can reactivate later

**Priority:** P0 (MVP)

---

### US-A-004: Reset User Password

**As an** Admin  
**I want to** reset a user's password  
**So that** they can regain access if forgotten

**Acceptance Criteria:**
- [ ] Can set new password for user
- [ ] User must change password on next login (optional)
- [ ] Action logged in audit

**Priority:** P1 (Should Have)

---

### US-A-005: View All Users

**As an** Admin  
**I want to** see all users in the system  
**So that** I can manage access

**Acceptance Criteria:**
- [ ] List of all users
- [ ] Shows name, username, role, status
- [ ] Can filter by role
- [ ] Can filter by active/inactive

**Priority:** P0 (MVP)

---

## Clinic Settings

### US-A-006: Configure Clinic Profile

**As an** Admin  
**I want to** set up the clinic's profile  
**So that** it appears on documents

**Acceptance Criteria:**
- [ ] Can enter clinic name
- [ ] Can enter address
- [ ] Can enter phone, email
- [ ] Can upload logo
- [ ] Settings used in prescriptions, invoices, receipts

**Priority:** P0 (MVP)

---

### US-A-007: Configure Prescription Header

**As an** Admin  
**I want to** customize the prescription header  
**So that** prescriptions have the correct clinic branding

**Acceptance Criteria:**
- [ ] Can set header text
- [ ] Can include logo
- [ ] Preview available
- [ ] Applied to all new prescriptions

**Priority:** P0 (MVP)

---

### US-A-008: Configure Invoice Header

**As an** Admin  
**I want to** customize the invoice/receipt header  
**So that** billing documents have correct branding

**Acceptance Criteria:**
- [ ] Can set header text
- [ ] Can include logo
- [ ] Can set footer text (terms, etc.)
- [ ] Applied to all new invoices/receipts

**Priority:** P0 (MVP)

---

## Billing Administration

### US-A-009: Cancel Invoice

**As an** Admin  
**I want to** cancel an issued invoice  
**So that** errors can be corrected

**Acceptance Criteria:**
- [ ] Can cancel invoice (only if not fully paid)
- [ ] Must enter cancellation reason
- [ ] Cancelled invoice retained for audit
- [ ] Patient balance updated
- [ ] Action logged

**Priority:** P1 (Should Have)

---

### US-A-010: View All Invoices

**As an** Admin  
**I want to** see all invoices  
**So that** I can monitor billing

**Acceptance Criteria:**
- [ ] List of all invoices
- [ ] Can filter by status, date range, patient
- [ ] Shows totals and balances
- [ ] Can export to Excel

**Priority:** P1 (Should Have)

---

## Reports

### US-A-011: View Daily Collections Report

**As an** Admin  
**I want to** see daily collection summary  
**So that** I can monitor revenue

**Acceptance Criteria:**
- [ ] Total collections for selected date
- [ ] Breakdown by payment mode
- [ ] List of individual payments
- [ ] Can select date range
- [ ] Can export to Excel/PDF

**Priority:** P0 (MVP)

---

### US-A-012: View Outstanding Payments Report

**As an** Admin  
**I want to** see all outstanding balances  
**So that** I can follow up on collections

**Acceptance Criteria:**
- [ ] List of patients with outstanding balance
- [ ] Shows invoice details and amounts
- [ ] Sorted by amount or age
- [ ] Can export to Excel

**Priority:** P0 (MVP)

---

### US-A-013: View Patient Statistics

**As an** Admin  
**I want to** see patient statistics  
**So that** I can understand clinic growth

**Acceptance Criteria:**
- [ ] Total patients registered
- [ ] New patients in period
- [ ] Total visits in period
- [ ] Can select date range

**Priority:** P1 (Should Have)

---

### US-A-014: View Upcoming Follow-ups Report

**As an** Admin  
**I want to** see scheduled follow-ups  
**So that** I can ensure patients are contacted

**Acceptance Criteria:**
- [ ] List of upcoming follow-ups
- [ ] Shows patient, date, dentist
- [ ] Can filter by date range
- [ ] Can filter by dentist

**Priority:** P0 (MVP)

---

## Backup & Recovery

### US-A-015: Configure Backup Schedule

**As an** Admin  
**I want to** configure automatic backups  
**So that** data is protected

**Acceptance Criteria:**
- [ ] Can set backup time (e.g., 11 PM daily)
- [ ] Can select backup destination (local folder, OneDrive, Google Drive)
- [ ] Can set retention period
- [ ] Settings saved

**Priority:** P1 (Should Have)

---

### US-A-016: Run Manual Backup

**As an** Admin  
**I want to** run a backup manually  
**So that** I can create a backup before major changes

**Acceptance Criteria:**
- [ ] Can trigger backup immediately
- [ ] Shows backup progress
- [ ] Notifies on completion
- [ ] Backup includes database and documents

**Priority:** P0 (MVP)

---

### US-A-017: View Backup History

**As an** Admin  
**I want to** see backup history  
**So that** I can verify backups are running

**Acceptance Criteria:**
- [ ] List of recent backups
- [ ] Shows date, time, size, status
- [ ] Shows destination
- [ ] Highlights failures

**Priority:** P1 (Should Have)

---

### US-A-018: Restore from Backup

**As an** Admin  
**I want to** restore data from a backup  
**So that** I can recover from data loss

**Acceptance Criteria:**
- [ ] Can select backup file
- [ ] Warning shown about data overwrite
- [ ] Restore process runs
- [ ] System restarts after restore

**Priority:** P0 (MVP)

---

## Audit & Security

### US-A-019: View Audit Log

**As an** Admin  
**I want to** see the audit log  
**So that** I can track who did what

**Acceptance Criteria:**
- [ ] List of audit events
- [ ] Shows user, action, entity, timestamp
- [ ] Can filter by user, action, date
- [ ] Can search by entity
- [ ] Cannot modify or delete logs

**Priority:** P1 (Should Have)

---

### US-A-020: Force Logout User

**As an** Admin  
**I want to** force logout a user  
**So that** I can terminate their session if needed

**Acceptance Criteria:**
- [ ] Can see active sessions
- [ ] Can terminate specific session
- [ ] User is logged out immediately
- [ ] Action logged

**Priority:** P2 (Nice to Have)

---

## Data Management

### US-A-021: Export Patient Data

**As an** Admin  
**I want to** export all data for a patient  
**So that** I can provide records if requested

**Acceptance Criteria:**
- [ ] Can select patient
- [ ] Export includes all records, documents
- [ ] Export in standard format (PDF + files)
- [ ] Action logged

**Priority:** P2 (Nice to Have)

---

### US-A-022: Delete Patient (Soft)

**As an** Admin  
**I want to** mark a patient as inactive  
**So that** they don't appear in searches

**Acceptance Criteria:**
- [ ] Can mark patient as inactive
- [ ] Patient hidden from normal searches
- [ ] All records retained
- [ ] Can reactivate if needed
- [ ] Action logged

**Priority:** P2 (Nice to Have)

---

## Related Documents

- [Receptionist User Stories](receptionist.md)
- [Dentist User Stories](dentist.md)
- [PRD](../prd.md)
