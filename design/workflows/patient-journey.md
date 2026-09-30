# Patient Journey Workflow

---

## Overview

This document describes the end-to-end patient journey from registration to follow-up.

---

## High-Level Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Patient    │    │  Reception   │    │   Dentist    │    │   Billing    │
│   Arrives    │───►│  Check-in    │───►│ Consultation │───►│   Payment    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                    │
                    ┌──────────────┐    ┌──────────────┐            │
                    │  Follow-up   │◄───│   Receipt    │◄───────────┘
                    │  Scheduled   │    │   Issued     │
                    └──────────────┘    └──────────────┘
```

---

## Detailed Workflow

### 1. Patient Arrival & Check-in

**Actor:** Receptionist

```
┌─────────────────────────────────────────────────────────────────┐
│                     PATIENT ARRIVAL                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Search Patient  │
                    │ (Name/Mobile)   │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │ Patient Found  │           │ New Patient    │
     └───────┬────────┘           └───────┬────────┘
             │                            │
             │                            ▼
             │                   ┌────────────────┐
             │                   │ Register New   │
             │                   │ Patient        │
             │                   │ - Name         │
             │                   │ - Mobile       │
             │                   │ - Gender       │
             │                   │ - DOB/Age      │
             │                   │ - Address      │
             │                   │ - Allergies    │
             │                   │ - Conditions   │
             │                   └───────┬────────┘
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Has Appointment│
                  │ Today?         │
                  └───────┬────────┘
                          │
           ┌──────────────┴──────────────┐
           │                             │
           ▼                             ▼
  ┌────────────────┐           ┌────────────────┐
  │ Yes: Mark as   │           │ No: Create     │
  │ "Waiting"      │           │ Walk-in Appt   │
  └───────┬────────┘           └───────┬────────┘
          │                            │
          └─────────────┬──────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ Patient Added  │
               │ to Queue       │
               └────────────────┘
```

---

### 2. Consultation

**Actor:** Dentist

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONSULTATION                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Select Patient  │
                    │ from Queue      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Mark Appointment│
                    │ "In Progress"   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Create Visit    │
                    │ Record          │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Review Patient  │
                    │ History &       │
                    │ Medical Alerts  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Record Chief    │
                    │ Complaint       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Clinical        │
                    │ Examination     │
                    │ - Dental Chart  │
                    │ - Findings      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Record          │
                    │ Diagnosis       │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │ Prescription   │           │ Treatment Plan │
     │ Required?      │           │ Required?      │
     └───────┬────────┘           └───────┬────────┘
             │                            │
             ▼                            ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ Create          │         │ Create          │
    │ Prescription    │         │ Treatment Plan  │
    │ - Medicines     │         │ - Procedures    │
    │ - Dosage        │         │ - Costs         │
    │ - Instructions  │         │ - Sessions      │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             ▼                           │
    ┌─────────────────┐                  │
    │ Print/Save      │                  │
    │ Prescription    │                  │
    └────────┬────────┘                  │
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Upload         │
                  │ Documents?     │
                  │ (X-rays, etc.) │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Schedule       │
                  │ Follow-up?     │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Complete Visit │
                  │ Mark "Done"    │
                  └────────────────┘
```

---

### 3. Billing & Payment

**Actor:** Receptionist / Billing Staff

```
┌─────────────────────────────────────────────────────────────────┐
│                     BILLING & PAYMENT                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Patient Ready   │
                    │ for Billing     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Has Treatment   │
                    │ Plan?           │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │ Yes: Generate  │           │ No: Create     │
     │ Invoice from   │           │ Ad-hoc Invoice │
     │ Treatment Plan │           │                │
     └───────┬────────┘           └───────┬────────┘
             │                            │
             └─────────────┬──────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Review Invoice │
                  │ - Line Items   │
                  │ - Amounts      │
                  │ - Discount?    │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Issue Invoice  │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Collect        │
                  │ Payment        │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Select Payment │
                  │ Mode           │
                  │ - Cash         │
                  │ - UPI          │
                  │ - Card         │
                  │ - Bank Transfer│
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Full Payment?  │
                  └───────┬────────┘
                          │
           ┌──────────────┴──────────────┐
           │                             │
           ▼                             ▼
  ┌────────────────┐           ┌────────────────┐
  │ Yes: Mark      │           │ No: Record     │
  │ Invoice PAID   │           │ Partial Payment│
  └───────┬────────┘           │ Track Balance  │
          │                    └───────┬────────┘
          │                            │
          └─────────────┬──────────────┘
                        │
                        ▼
               ┌────────────────┐
               │ Generate       │
               │ Receipt        │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │ Print Receipt  │
               └────────────────┘
```

---

### 4. Follow-up Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     FOLLOW-UP CYCLE                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Follow-up Date  │
                    │ Approaches      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ View Upcoming   │
                    │ Follow-ups      │
                    │ Report          │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Patient Arrives │
                    │ for Follow-up   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Repeat          │
                    │ Consultation    │
                    │ Flow            │
                    └─────────────────┘
```

---

## State Transitions

### Appointment States

```
SCHEDULED ──► WAITING ──► IN_PROGRESS ──► COMPLETED
    │                          │
    │                          └──► CANCELLED
    │
    └──► CANCELLED
    │
    └──► NO_SHOW
```

### Visit States

```
IN_PROGRESS ──► COMPLETED
```

### Treatment Plan States

```
PROPOSED ──► APPROVED ──► IN_PROGRESS ──► COMPLETED
    │            │              │
    └────────────┴──────────────┴──► CANCELLED
```

### Invoice States

```
DRAFT ──► ISSUED ──► PARTIALLY_PAID ──► PAID
             │
             └──► CANCELLED
```

---

## Key Decision Points

| Decision | Options | Next Step |
|----------|---------|-----------|
| New or existing patient? | New | Register patient |
| | Existing | Search and select |
| Has appointment? | Yes | Mark as waiting |
| | No | Create walk-in |
| Prescription needed? | Yes | Create prescription |
| | No | Skip |
| Treatment needed? | Yes | Create treatment plan |
| | No | Skip |
| Full payment? | Yes | Mark invoice paid |
| | No | Record partial, track balance |
| Follow-up needed? | Yes | Schedule appointment |
| | No | Complete |

---

## Related Documents

- [Billing Workflow](billing-workflow.md)
- [Prescription Workflow](prescription-workflow.md)
- [User Stories](../../docs/requirements/user-stories/)
