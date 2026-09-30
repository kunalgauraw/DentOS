# DentOS Release Plan

---

## Overview

This document outlines the sprint-by-sprint delivery plan for DentOS MVP.

---

## Phase 0: Product Definition (Weeks 1-3)

### Week 1-2: Requirements & Design

| Task | Owner | Status |
|------|-------|--------|
| Finalize PRD | PM | In Progress |
| Define user stories | PM | Not Started |
| Document business rules | PM | Not Started |
| Create workflow diagrams | PM/UX | Not Started |
| Design wireframes | UX | Not Started |
| Review with stakeholders | PM | Not Started |

### Week 2-3: Technical Design

| Task | Owner | Status |
|------|-------|--------|
| Define domain model | Architect | Not Started |
| Design database schema | Architect | Not Started |
| Specify API contracts | Architect | Not Started |
| Document security model | Architect | Draft |
| Create ADRs | Architect | Not Started |
| Setup project scaffolding | Dev | Not Started |

---

## Phase 1: MVP Development (Weeks 4-15)

### Sprint 1-2: Foundation (Weeks 4-5)

**Goal:** Project setup and authentication

| Task | Story Points |
|------|--------------|
| Setup React project with TypeScript | 3 |
| Setup FastAPI project | 3 |
| Setup PostgreSQL with Docker | 2 |
| Implement user authentication | 5 |
| Implement role-based authorization | 5 |
| Create basic UI shell with navigation | 3 |
| Setup CI/CD pipeline | 3 |

**Sprint Total:** 24 points

---

### Sprint 3-4: Patient Module (Weeks 6-7)

**Goal:** Complete patient management

| Task | Story Points |
|------|--------------|
| Patient registration form | 5 |
| Patient search functionality | 3 |
| Patient profile view | 3 |
| Patient edit functionality | 3 |
| Patient timeline view | 5 |
| Medical alerts display | 2 |
| Patient API endpoints | 5 |

**Sprint Total:** 26 points

---

### Sprint 5-6: Clinical Module (Weeks 8-9)

**Goal:** Appointments and clinical encounters

| Task | Story Points |
|------|--------------|
| Appointment booking | 5 |
| Appointment calendar view | 5 |
| Queue management | 3 |
| Visit creation | 3 |
| Clinical notes form | 5 |
| Dental chart UI | 8 |
| Dental chart persistence | 5 |

**Sprint Total:** 34 points

---

### Sprint 7-8: Prescription & Treatment (Weeks 10-11)

**Goal:** Prescriptions and treatment plans

| Task | Story Points |
|------|--------------|
| Prescription form | 5 |
| Medicine entry (multi-line) | 3 |
| Prescription print layout | 5 |
| Prescription PDF generation | 3 |
| Treatment plan form | 5 |
| Treatment status tracking | 3 |
| Treatment history view | 3 |

**Sprint Total:** 27 points

---

### Sprint 9-10: Billing Module (Weeks 12-13)

**Goal:** Complete billing workflow

| Task | Story Points |
|------|--------------|
| Invoice creation | 5 |
| Invoice from treatment plan | 3 |
| Payment recording | 5 |
| Multiple payment modes | 2 |
| Partial payment support | 3 |
| Receipt generation | 3 |
| Receipt print layout | 3 |
| Outstanding balance tracking | 3 |

**Sprint Total:** 27 points

---

### Sprint 11-12: Documents & Reports (Weeks 14-15)

**Goal:** Document storage and reporting

| Task | Story Points |
|------|--------------|
| Document upload | 5 |
| Document viewer | 3 |
| Document linking to patient | 2 |
| Daily collections report | 3 |
| Outstanding payments report | 3 |
| Follow-ups report | 3 |
| Patient statistics | 3 |
| Automated backup | 8 |

**Sprint Total:** 30 points

---

## Phase 2: Stabilization (Weeks 16-18)

| Task | Owner | Status |
|------|-------|--------|
| End-to-end testing | QA | Not Started |
| Bug fixes | Dev | Not Started |
| Performance optimization | Dev | Not Started |
| Documentation completion | All | Not Started |
| Installer packaging | DevOps | Not Started |
| Pilot deployment | All | Not Started |

---

## Milestones

| Milestone | Target Date | Deliverable |
|-----------|-------------|-------------|
| M0: Design Complete | Week 3 | All design docs approved |
| M1: Foundation Ready | Week 5 | Auth working, project setup complete |
| M2: Patient Module | Week 7 | Patient CRUD complete |
| M3: Clinical Module | Week 9 | Visits and dental chart working |
| M4: Prescription & Treatment | Week 11 | Prescriptions and treatments working |
| M5: Billing Module | Week 13 | Full billing workflow |
| M6: MVP Complete | Week 15 | All MVP features working |
| M7: Production Ready | Week 18 | Tested, documented, packaged |

---

## Dependencies

| Dependency | Impact | Mitigation |
|------------|--------|------------|
| Stakeholder availability for reviews | Delays in approval | Schedule reviews in advance |
| Printer testing | Print layouts may need adjustment | Test early with common printers |
| Cloud backup integration | OneDrive/Google Drive API | Start integration in Sprint 10 |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | High | High | Strict scope document, defer features |
| Dental chart complexity | Medium | Medium | Start simple, iterate |
| Print layout issues | Medium | Low | Test with multiple printers early |
| Offline sync issues | Low | High | No sync in MVP, local-only |

---

## Related Documents

- [Product Roadmap](../product/roadmap.md)
- [Backlog](backlog.md)
- [PRD](../requirements/prd.md)
