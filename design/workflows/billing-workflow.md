# Billing Workflow

---

## Overview

This document describes the billing workflow from invoice creation to payment collection and receipt generation.

---

## High-Level Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Create     │    │    Issue     │    │   Collect    │    │   Generate   │
│   Invoice    │───►│   Invoice    │───►│   Payment    │───►│   Receipt    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## Detailed Workflow

### 1. Invoice Creation

```
┌─────────────────────────────────────────────────────────────────┐
│                     INVOICE CREATION                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Select Patient  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Invoice Source? │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ From Treatment │  │ From Visit     │  │ Ad-hoc         │
│ Plan           │  │ (Consultation) │  │ (Manual Entry) │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Select         │  │ Add            │  │ Add Line Items │
│ Procedures     │  │ Consultation   │  │ Manually       │
│ to Invoice     │  │ Fee            │  │ - Description  │
└───────┬────────┘  └───────┬────────┘  │ - Amount       │
        │                   │           └───────┬────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │ Invoice Items  │
                   │ Listed         │
                   │                │
                   │ Subtotal: XXX  │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │ Apply          │
                   │ Discount?      │
                   └───────┬────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
   ┌────────────────┐           ┌────────────────┐
   │ Yes: Enter     │           │ No: Skip       │
   │ Discount       │           │                │
   │ - Amount or %  │           │                │
   └───────┬────────┘           └───────┬────────┘
           │                            │
           └─────────────┬──────────────┘
                         │
                         ▼
                ┌────────────────┐
                │ Calculate      │
                │ Final Total    │
                │                │
                │ Subtotal: XXX  │
                │ Discount: -XX  │
                │ Tax: +XX       │
                │ ─────────────  │
                │ Total: XXX     │
                └───────┬────────┘
                        │
                        ▼
                ┌────────────────┐
                │ Save as Draft  │
                │ or Issue?      │
                └───────┬────────┘
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
┌────────────────┐           ┌────────────────┐
│ Save Draft     │           │ Issue Invoice  │
│ (Edit Later)   │           │ (Final)        │
└────────────────┘           └───────┬────────┘
                                     │
                                     ▼
                            ┌────────────────┐
                            │ Invoice Number │
                            │ Generated      │
                            │ INV-XXXXXX     │
                            └────────────────┘
```

---

### 2. Payment Collection

```
┌─────────────────────────────────────────────────────────────────┐
│                     PAYMENT COLLECTION                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Select Invoice  │
                    │ (Issued/Partial)│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ View Invoice    │
                    │ Details         │
                    │                 │
                    │ Total: 5000     │
                    │ Paid: 2000      │
                    │ Balance: 3000   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Enter Payment   │
                    │ Amount          │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Amount <=       │
                    │ Balance?        │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │ Yes: Proceed   │           │ No: Show Error │
     │                │           │ "Amount exceeds│
     │                │           │  balance"      │
     └───────┬────────┘           └────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ Select Payment  │
    │ Mode            │
    └────────┬────────┘
             │
    ┌────────┼────────┬────────────┬────────────┐
    │        │        │            │            │
    ▼        ▼        ▼            ▼            │
┌──────┐ ┌──────┐ ┌──────┐   ┌──────────┐      │
│ CASH │ │ UPI  │ │ CARD │   │ BANK     │      │
└──┬───┘ └──┬───┘ └──┬───┘   │ TRANSFER │      │
   │        │        │       └────┬─────┘      │
   │        │        │            │            │
   │        ▼        ▼            ▼            │
   │   ┌─────────────────────────────┐         │
   │   │ Enter Reference Number      │         │
   │   │ (Transaction ID / Ref No)   │         │
   │   └─────────────┬───────────────┘         │
   │                 │                         │
   └─────────────────┴─────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │ Confirm        │
            │ Payment        │
            └───────┬────────┘
                    │
                    ▼
            ┌────────────────┐
            │ Update Invoice │
            │                │
            │ Paid: +Amount  │
            │ Balance: -Amt  │
            └───────┬────────┘
                    │
                    ▼
            ┌────────────────┐
            │ Balance = 0?   │
            └───────┬────────┘
                    │
     ┌──────────────┴──────────────┐
     │                             │
     ▼                             ▼
┌────────────────┐       ┌────────────────┐
│ Yes: Mark      │       │ No: Mark       │
│ Invoice PAID   │       │ PARTIALLY_PAID │
└───────┬────────┘       └───────┬────────┘
        │                        │
        └────────────┬───────────┘
                     │
                     ▼
            ┌────────────────┐
            │ Generate       │
            │ Receipt        │
            │ RCP-XXXXXX     │
            └────────────────┘
```

---

### 3. Receipt Generation

```
┌─────────────────────────────────────────────────────────────────┐
│                     RECEIPT GENERATION                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Receipt Created │
                    │ Automatically   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────────────────────┐
                    │         RECEIPT                  │
                    │  ─────────────────────────────  │
                    │  Receipt No: RCP-000123         │
                    │  Date: 2024-01-15               │
                    │                                 │
                    │  Patient: John Doe              │
                    │  Invoice: INV-000456            │
                    │                                 │
                    │  Amount Received: Rs. 3,000     │
                    │  Payment Mode: UPI              │
                    │  Reference: TXN123456           │
                    │                                 │
                    │  Invoice Total: Rs. 5,000       │
                    │  Total Paid: Rs. 5,000          │
                    │  Balance: Rs. 0                 │
                    │                                 │
                    │  Received By: Reception Staff   │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                            ┌────────────────┐
                            │ Print Receipt? │
                            └───────┬────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
            ┌────────────────┐           ┌────────────────┐
            │ Print          │           │ Save/Email     │
            │ (Thermal/A4)   │           │ PDF            │
            └────────────────┘           └────────────────┘
```

---

## Invoice States

```
                              ┌─────────┐
                              │  DRAFT  │
                              └────┬────┘
                                   │
                                   │ Issue Invoice
                                   ▼
                              ┌─────────┐
                              │ ISSUED  │
                              └────┬────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    │ Partial Payment             │ Full Payment
                    ▼                             ▼
           ┌────────────────┐            ┌────────────────┐
           │ PARTIALLY_PAID │────────────│      PAID      │
           └────────────────┘            └────────────────┘
                    │
                    │ Remaining payments
                    └─────────────────────────────┘

           Any state (except PAID) can transition to:
                              ┌───────────┐
                              │ CANCELLED │
                              └───────────┘
```

---

## Business Rules

### Invoice Creation

| Rule | Description |
|------|-------------|
| INV-001 | Invoice number auto-generated on issue |
| INV-002 | Draft invoices can be edited |
| INV-003 | Issued invoices cannot be edited |
| INV-004 | Discount cannot exceed subtotal |
| INV-005 | At least one line item required |

### Payment Collection

| Rule | Description |
|------|-------------|
| PAY-001 | Payment amount cannot exceed balance |
| PAY-002 | Payment amount must be > 0 |
| PAY-003 | Receipt auto-generated on payment |
| PAY-004 | Reference required for non-cash payments |
| PAY-005 | Multiple payments allowed per invoice |

### Cancellation

| Rule | Description |
|------|-------------|
| CAN-001 | Only Admin can cancel invoice |
| CAN-002 | Paid invoices cannot be cancelled |
| CAN-003 | Cancellation reason required |
| CAN-004 | Cancelled invoices retained for audit |

---

## Reports Generated

| Report | Data |
|--------|------|
| Daily Collections | Sum of payments by date, grouped by mode |
| Outstanding Payments | Invoices with balance > 0 |
| Invoice Register | All invoices for period |
| Payment Register | All payments for period |

---

## Related Documents

- [Patient Journey](patient-journey.md)
- [Business Rules](../../docs/requirements/business-rules.md)
- [PRD - Billing Section](../../docs/requirements/prd.md)
