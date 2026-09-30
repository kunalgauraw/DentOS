# DentOS Database Schema

---

## Overview

This document defines the PostgreSQL database schema for DentOS.

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Tables | snake_case, plural | `patients`, `treatment_plans` |
| Columns | snake_case | `patient_id`, `created_at` |
| Primary Keys | `id` | `id UUID PRIMARY KEY` |
| Foreign Keys | `{table}_id` | `patient_id`, `user_id` |
| Indexes | `idx_{table}_{column}` | `idx_patients_mobile` |
| Constraints | `{table}_{type}_{column}` | `patients_uq_mobile` |

---

## Schema Definition

### users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('RECEPTIONIST', 'DENTIST', 'ADMIN')),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
```

---

### patients

```sql
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_number VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    date_of_birth DATE,
    age INTEGER,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    address TEXT,
    email VARCHAR(100),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(15),
    allergies TEXT,
    medical_conditions TEXT,
    current_medications TEXT,
    notes TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL REFERENCES users(id)
);

CREATE INDEX idx_patients_patient_number ON patients(patient_number);
CREATE INDEX idx_patients_name ON patients(name);
CREATE INDEX idx_patients_mobile ON patients(mobile);
CREATE INDEX idx_patients_created_at ON patients(created_at);
```

---

### appointments

```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    user_id UUID REFERENCES users(id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    type VARCHAR(20) NOT NULL CHECK (type IN ('CONSULTATION', 'FOLLOW_UP', 'PROCEDURE')),
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED' 
        CHECK (status IN ('SCHEDULED', 'WAITING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
    notes TEXT,
    cancellation_reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL REFERENCES users(id)
);

CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_user_id ON appointments(user_id);
```

---

### visits

```sql
CREATE TABLE visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_number VARCHAR(20) NOT NULL UNIQUE,
    patient_id UUID NOT NULL REFERENCES patients(id),
    appointment_id UUID REFERENCES appointments(id),
    user_id UUID NOT NULL REFERENCES users(id),
    visit_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    chief_complaint TEXT,
    history TEXT,
    clinical_findings TEXT,
    diagnosis TEXT,
    advice TEXT,
    notes TEXT,
    follow_up_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'IN_PROGRESS' 
        CHECK (status IN ('IN_PROGRESS', 'COMPLETED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_visits_patient_id ON visits(patient_id);
CREATE INDEX idx_visits_visit_number ON visits(visit_number);
CREATE INDEX idx_visits_visit_date ON visits(visit_date);
CREATE INDEX idx_visits_user_id ON visits(user_id);
```

---

### dental_charts

```sql
CREATE TABLE dental_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    tooth_number INTEGER NOT NULL CHECK (tooth_number BETWEEN 1 AND 85),
    status VARCHAR(30) NOT NULL DEFAULT 'HEALTHY'
        CHECK (status IN ('HEALTHY', 'CARIES', 'MISSING', 'RCT', 'CROWN', 'IMPLANT', 'EXTRACTION_PLANNED')),
    notes TEXT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID NOT NULL REFERENCES users(id),
    UNIQUE(patient_id, tooth_number)
);

CREATE INDEX idx_dental_charts_patient_id ON dental_charts(patient_id);
```

---

### prescriptions

```sql
CREATE TABLE prescriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rx_number VARCHAR(20) NOT NULL UNIQUE,
    patient_id UUID NOT NULL REFERENCES patients(id),
    visit_id UUID NOT NULL REFERENCES visits(id),
    user_id UUID NOT NULL REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prescriptions_patient_id ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_rx_number ON prescriptions(rx_number);
CREATE INDEX idx_prescriptions_visit_id ON prescriptions(visit_id);
```

---

### prescription_medicines

```sql
CREATE TABLE prescription_medicines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prescription_id UUID NOT NULL REFERENCES prescriptions(id) ON DELETE CASCADE,
    medicine_name VARCHAR(200) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    duration VARCHAR(100),
    instructions TEXT,
    sequence INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_prescription_medicines_prescription_id ON prescription_medicines(prescription_id);
```

---

### treatment_plans

```sql
CREATE TABLE treatment_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_number VARCHAR(20) NOT NULL UNIQUE,
    patient_id UUID NOT NULL REFERENCES patients(id),
    visit_id UUID REFERENCES visits(id),
    created_by UUID NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'PROPOSED'
        CHECK (status IN ('PROPOSED', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    total_cost DECIMAL(12, 2) NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_treatment_plans_patient_id ON treatment_plans(patient_id);
CREATE INDEX idx_treatment_plans_plan_number ON treatment_plans(plan_number);
CREATE INDEX idx_treatment_plans_status ON treatment_plans(status);
```

---

### treatment_procedures

```sql
CREATE TABLE treatment_procedures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    treatment_plan_id UUID NOT NULL REFERENCES treatment_plans(id) ON DELETE CASCADE,
    procedure_name VARCHAR(200) NOT NULL,
    tooth_number INTEGER CHECK (tooth_number BETWEEN 1 AND 85),
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0,
    sessions INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'PROPOSED'
        CHECK (status IN ('PROPOSED', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    notes TEXT,
    sequence INTEGER NOT NULL DEFAULT 1,
    completed_at TIMESTAMP
);

CREATE INDEX idx_treatment_procedures_plan_id ON treatment_procedures(treatment_plan_id);
CREATE INDEX idx_treatment_procedures_status ON treatment_procedures(status);
```

---

### invoices

```sql
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number VARCHAR(20) NOT NULL UNIQUE,
    patient_id UUID NOT NULL REFERENCES patients(id),
    treatment_plan_id UUID REFERENCES treatment_plans(id),
    created_by UUID NOT NULL REFERENCES users(id),
    invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
    subtotal DECIMAL(12, 2) NOT NULL DEFAULT 0,
    discount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    tax DECIMAL(12, 2) NOT NULL DEFAULT 0,
    total DECIMAL(12, 2) NOT NULL DEFAULT 0,
    amount_paid DECIMAL(12, 2) NOT NULL DEFAULT 0,
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT'
        CHECK (status IN ('DRAFT', 'ISSUED', 'PARTIALLY_PAID', 'PAID', 'CANCELLED')),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoices_patient_id ON invoices(patient_id);
CREATE INDEX idx_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_invoice_date ON invoices(invoice_date);
```

---

### invoice_items

```sql
CREATE TABLE invoice_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    procedure_id UUID REFERENCES treatment_procedures(id),
    description VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
    amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    sequence INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_invoice_items_invoice_id ON invoice_items(invoice_id);
```

---

### payments

```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    receipt_number VARCHAR(20) NOT NULL UNIQUE,
    invoice_id UUID NOT NULL REFERENCES invoices(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_mode VARCHAR(20) NOT NULL 
        CHECK (payment_mode IN ('CASH', 'UPI', 'CARD', 'BANK_TRANSFER')),
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    reference VARCHAR(100),
    notes TEXT,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_invoice_id ON payments(invoice_id);
CREATE INDEX idx_payments_receipt_number ON payments(receipt_number);
CREATE INDEX idx_payments_payment_date ON payments(payment_date);
```

---

### documents

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    visit_id UUID REFERENCES visits(id),
    document_type VARCHAR(20) NOT NULL 
        CHECK (document_type IN ('XRAY', 'PHOTO', 'CONSENT', 'REPORT', 'OTHER')),
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    description TEXT,
    uploaded_by UUID NOT NULL REFERENCES users(id),
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_patient_id ON documents(patient_id);
CREATE INDEX idx_documents_visit_id ON documents(visit_id);
CREATE INDEX idx_documents_document_type ON documents(document_type);
```

---

### audit_logs

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    changes JSONB,
    ip_address VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
```

---

### clinic_settings

```sql
CREATE TABLE clinic_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_name VARCHAR(200) NOT NULL,
    address TEXT,
    phone VARCHAR(15),
    email VARCHAR(100),
    logo_path VARCHAR(500),
    prescription_header TEXT,
    invoice_header TEXT,
    working_hours JSONB,
    backup_schedule JSONB,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

### sequences

For generating sequential numbers:

```sql
CREATE SEQUENCE patient_number_seq START 1;
CREATE SEQUENCE visit_number_seq START 1;
CREATE SEQUENCE rx_number_seq START 1;
CREATE SEQUENCE plan_number_seq START 1;
CREATE SEQUENCE invoice_number_seq START 1;
CREATE SEQUENCE receipt_number_seq START 1;
```

---

## Functions

### Generate Patient Number

```sql
CREATE OR REPLACE FUNCTION generate_patient_number()
RETURNS VARCHAR(20) AS $$
BEGIN
    RETURN 'PAT-' || LPAD(nextval('patient_number_seq')::TEXT, 6, '0');
END;
$$ LANGUAGE plpgsql;
```

### Update Timestamp Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_visits_updated_at BEFORE UPDATE ON visits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_treatment_plans_updated_at BEFORE UPDATE ON treatment_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

---

## Initial Data

### Default Admin User

```sql
INSERT INTO users (username, password_hash, role, name, email)
VALUES (
    'admin',
    '$2b$12$...', -- bcrypt hash of default password
    'ADMIN',
    'Administrator',
    'admin@clinic.local'
);
```

### Default Clinic Settings

```sql
INSERT INTO clinic_settings (clinic_name, address)
VALUES ('My Dental Clinic', 'Address to be configured');
```

---

## Related Documents

- [Domain Model](domain-model.md)
- [API Specification](api-spec.md)
- [Architecture Overview](overview.md)
