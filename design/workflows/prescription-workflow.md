# Prescription Workflow

---

## Overview

This document describes the prescription creation workflow from clinical encounter to print/PDF generation.

---

## High-Level Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   During     │    │    Add       │    │   Review &   │    │   Print/     │
│   Visit      │───►│   Medicines  │───►│   Save       │───►│   Export     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## Detailed Workflow

### 1. Prescription Creation

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESCRIPTION CREATION                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ During Active   │
                    │ Visit           │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Click "Create   │
                    │ Prescription"   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Patient Info    │
                    │ Auto-filled     │
                    │ - Name          │
                    │ - Age/Gender    │
                    │ - Allergies ⚠️  │
                    └────────┬────────┘
                             │
                             ▼
            ┌────────────────────────────────┐
            │        ADD MEDICINES           │
            │  ┌──────────────────────────┐  │
            │  │ Medicine Name            │  │
            │  │ [________________________]│  │
            │  │                          │  │
            │  │ Dosage      Frequency    │  │
            │  │ [500mg]     [1-0-1]      │  │
            │  │                          │  │
            │  │ Duration    Instructions │  │
            │  │ [5 days]    [After food] │  │
            │  │                          │  │
            │  │ [+ Add Another Medicine] │  │
            │  └──────────────────────────┘  │
            └───────────────┬────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │ Add More       │
                   │ Medicines?     │
                   └───────┬────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
   ┌────────────────┐           ┌────────────────┐
   │ Yes: Add       │           │ No: Continue   │
   │ Another Row    │           │                │
   └───────┬────────┘           └───────┬────────┘
           │                            │
           └──────────────┬─────────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ Add General    │
                 │ Instructions?  │
                 │ (Optional)     │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Review         │
                 │ Prescription   │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Save           │
                 │ Prescription   │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Rx Number      │
                 │ Generated      │
                 │ RX-XXXXXX      │
                 └────────────────┘
```

---

### 2. Medicine Entry

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEDICINE ENTRY                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Enter Medicine  │
                    │ Name            │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Free Text Entry │
                    │ (MVP)           │
                    │                 │
                    │ Future: Auto-   │
                    │ complete from   │
                    │ medicine master │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Enter Dosage    │
                    │ e.g., 500mg,    │
                    │ 10ml, 1 tablet  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Enter Frequency │
                    │ Common formats: │
                    │ - 1-0-1         │
                    │ - 1-1-1         │
                    │ - 0-0-1         │
                    │ - Once daily    │
                    │ - Twice daily   │
                    │ - As needed     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Enter Duration  │
                    │ e.g., 5 days,   │
                    │ 1 week, 2 weeks │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Special         │
                    │ Instructions    │
                    │ (Optional)      │
                    │ e.g., After     │
                    │ food, Before    │
                    │ sleep           │
                    └────────────────┘
```

---

### 3. Print/Export

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRINT / EXPORT                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Prescription    │
                    │ Saved           │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Output Options  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────────┐ ┌────────────┐ ┌────────────┐
     │ Print          │ │ Save PDF   │ │ View Only  │
     │ (A4/A5)        │ │            │ │            │
     └───────┬────────┘ └─────┬──────┘ └─────┬──────┘
             │                │              │
             ▼                ▼              │
     ┌────────────────┐ ┌────────────┐       │
     │ Print Dialog   │ │ Download   │       │
     │ - Printer      │ │ PDF File   │       │
     │ - Copies       │ │            │       │
     └───────┬────────┘ └─────┬──────┘       │
             │                │              │
             └────────────────┴──────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Prescription    │
                    │ Logged in       │
                    │ Patient History │
                    └─────────────────┘
```

---

## Prescription Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [CLINIC LOGO]     CLINIC NAME                                  │
│                    Address Line 1                               │
│                    Address Line 2                               │
│                    Phone: XXXXXXXXXX                            │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Rx No: RX-000123                    Date: 15-Jan-2024          │
│                                                                 │
│  Patient: John Doe                   Age/Gender: 35Y / Male     │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ℞                                                              │
│                                                                 │
│  1. Amoxicillin 500mg                                           │
│     1-0-1 x 5 days                                              │
│     After food                                                  │
│                                                                 │
│  2. Ibuprofen 400mg                                             │
│     1-0-1 x 3 days                                              │
│     After food, if pain                                         │
│                                                                 │
│  3. Chlorhexidine Mouthwash                                     │
│     Twice daily x 1 week                                        │
│     Rinse for 30 seconds, do not swallow                        │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Instructions:                                                  │
│  - Complete the full course of antibiotics                      │
│  - Avoid hot/cold food for 24 hours                             │
│  - Follow up after 1 week                                       │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│                                      Dr. Smith                  │
│                                      BDS, MDS                   │
│                                      Reg No: XXXXX              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Business Rules

### Prescription Creation

| Rule | Description |
|------|-------------|
| RX-001 | Prescription must be linked to a visit |
| RX-002 | At least one medicine required |
| RX-003 | Medicine name is required |
| RX-004 | Prescription number auto-generated |
| RX-005 | Prescribing doctor auto-captured |

### Medicine Entry

| Rule | Description |
|------|-------------|
| MED-001 | Dosage, frequency, duration recommended but optional |
| MED-002 | Medicines ordered by sequence |
| MED-003 | Free text entry (no master validation in MVP) |

### Print/Export

| Rule | Description |
|------|-------------|
| PRT-001 | Clinic header from settings |
| PRT-002 | Doctor details from user profile |
| PRT-003 | PDF stored with patient documents |
| PRT-004 | Print action logged in audit |

---

## Allergy Warning

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  ALLERGY ALERT                                              │
│  ─────────────────────────────────────────────────────────────  │
│  This patient has the following allergies:                      │
│                                                                 │
│  • Penicillin                                                   │
│  • Sulfa drugs                                                  │
│                                                                 │
│  Please verify prescribed medicines are safe.                   │
│                                                                 │
│  [Acknowledge & Continue]                                       │
└─────────────────────────────────────────────────────────────────┘
```

**Note:** MVP shows warning only. Future versions may include drug-allergy interaction checking.

---

## Prescription History

Prescriptions are accessible from:

1. **Patient Timeline** - All prescriptions for patient
2. **Visit Details** - Prescriptions from specific visit
3. **Prescription Search** - By Rx number or date range

---

## Related Documents

- [Patient Journey](patient-journey.md)
- [PRD - Prescription Section](../../docs/requirements/prd.md)
- [Domain Model](../../docs/architecture/domain-model.md)
