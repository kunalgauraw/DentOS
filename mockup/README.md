# DentOS Static Mockup

This folder contains a static HTML/CSS mockup of the DentOS application for visualization and feedback purposes.

## How to View

1. Open `index.html` in any web browser
2. Click through the screens to visualize the application flow

**Or simply double-click `index.html` in Windows Explorer.**

## Screens Included (18 pages)

| Screen | File | Description |
|--------|------|-------------|
| Index | `index.html` | Navigation to all screens |
| Login | `login.html` | Authentication screen |
| Dashboard | `dashboard.html` | Main overview with stats and queue |
| Patient List | `patients.html` | Search and browse patients |
| New Patient | `patient-new.html` | Patient registration form |
| Patient Profile | `patient-profile.html` | Patient details and timeline |
| Consultation | `consultation.html` | Visit and clinical notes |
| Dental Chart | `dental-chart.html` | Tooth status visualization |
| Prescription | `prescription.html` | Medicine prescription form |
| Treatment Plan | `treatment-plan.html` | Procedures, costs, sessions |
| Appointments | `appointments.html` | Calendar and queue view |
| Book Appointment | `appointment-new.html` | Appointment booking form |
| Billing | `billing.html` | Invoice list |
| New Invoice | `invoice-new.html` | Invoice creation form |
| Payment | `payment.html` | Payment collection |
| Reports | `reports.html` | Collections, statistics, follow-ups |
| Settings | `settings.html` | Clinic info, backup configuration |
| User Management | `users.html` | Users and role permissions |

## Navigation Flow

```
Login → Dashboard
           ↓
    ┌──────┴──────┬──────────────┐
    ↓             ↓              ↓
Patients    Appointments     Settings
    ↓             ↓              ↓
Patient      Book Appt       Users
Profile       Calendar       Backup
    ↓
Consultation
    ↓
┌───┴───┬────────┐
↓       ↓        ↓
Dental  Rx    Treatment
Chart         Plan
    ↓
Billing → Invoice → Payment → Receipt
    ↓
Reports (Collections, Stats, Follow-ups)
```

## MVP Requirements Coverage

| Requirement | Screen | Status |
|-------------|--------|--------|
| Patient Registry | patients, patient-new, patient-profile | ✅ |
| Appointments | appointments, appointment-new | ✅ |
| Clinical Encounters | consultation | ✅ |
| Dental Chart | dental-chart | ✅ |
| Prescription | prescription | ✅ |
| Treatment Plan | treatment-plan | ✅ |
| Billing | billing, invoice-new, payment | ✅ |
| Reports | reports (with patient stats) | ✅ |
| User Management | users | ✅ |
| Backup | settings | ✅ |

## What This Mockup IS

- Visual representation of UI layout
- Navigation flow demonstration
- Color scheme and styling preview
- Component design reference
- MVP requirements validation

## What This Mockup IS NOT

- Functional application (forms don't submit)
- Interactive prototype (no state management)
- Production code (not reusable)
- Mobile responsive (desktop only for now)

## Feedback Points

When reviewing, consider:

1. **Layout** - Is the information organized logically?
2. **Navigation** - Is it easy to find things?
3. **Forms** - Are the right fields included?
4. **Workflow** - Does the flow make sense?
5. **Missing Features** - What's not covered?

## Files

```
mockup/
├── index.html              ← Start here
├── login.html
├── dashboard.html
├── patients.html
├── patient-new.html
├── patient-profile.html
├── consultation.html
├── dental-chart.html
├── prescription.html
├── treatment-plan.html     ← NEW
├── appointments.html
├── appointment-new.html    ← NEW
├── billing.html
├── invoice-new.html
├── payment.html
├── reports.html            ← Updated with patient stats
├── settings.html           ← NEW
├── users.html              ← NEW
├── css/
│   └── styles.css          ← All styling
└── README.md               ← This file
```

## After Review

Once the mockup is approved:

1. This folder can be deleted
2. Actual development begins in `frontend/`
3. Mockup served its purpose - visualization before coding

---

**Note:** This mockup is separate from the actual codebase and will not affect Phase 1 development.
