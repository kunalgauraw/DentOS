"""Tests for billing (invoices and payments) endpoints"""


def create_test_patient_and_visit(client, auth_headers):
    """Helper to create a test patient and visit"""
    # Create patient
    patient_response = client.post(
        "/patients/",
        json={"full_name": "Billing Test", "mobile": "9876600001", "gender": "Male"},
        headers=auth_headers
    )
    patient_id = patient_response.json()["id"]
    
    # Create visit
    visit_response = client.post(
        "/visits/",
        json={"patient_id": patient_id, "chief_complaint": "Billing test"},
        headers=auth_headers
    )
    visit_id = visit_response.json()["id"]
    
    return patient_id, visit_id


def test_create_invoice(client, auth_headers):
    """Test creating an invoice"""
    patient_id, visit_id = create_test_patient_and_visit(client, auth_headers)
    
    response = client.post(
        "/invoices/",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "items": [
                {"description": "Consultation", "quantity": 1, "rate": 500, "amount": 500},
                {"description": "X-Ray", "quantity": 1, "rate": 300, "amount": 300}
            ],
            "discount": 50,
            "gst_percent": 0
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 800
    assert data["discount"] == 50
    assert data["total"] == 750
    assert data["status"] == "pending"
    assert data["invoice_id"].startswith("INV-")


def test_create_invoice_with_gst(client, auth_headers):
    """Test creating invoice with GST"""
    patient_id, visit_id = create_test_patient_and_visit(client, auth_headers)
    
    response = client.post(
        "/invoices/",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "items": [
                {"description": "Cosmetic procedure", "quantity": 1, "rate": 1000, "amount": 1000}
            ],
            "discount": 0,
            "gst_percent": 18
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["gst_amount"] == 180
    assert data["total"] == 1180


def test_collect_payment(client, auth_headers):
    """Test collecting payment for an invoice"""
    patient_id, visit_id = create_test_patient_and_visit(client, auth_headers)
    
    # Create invoice
    invoice_response = client.post(
        "/invoices/",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "items": [{"description": "Treatment", "quantity": 1, "rate": 1000, "amount": 1000}],
            "discount": 0,
            "gst_percent": 0
        },
        headers=auth_headers
    )
    invoice_id = invoice_response.json()["id"]
    
    # Collect payment
    response = client.post(
        "/payments/",
        json={
            "invoice_id": invoice_id,
            "patient_id": patient_id,
            "amount": 1000,
            "payment_mode": "cash"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 1000
    assert data["payment_mode"] == "cash"
    assert data["receipt_id"].startswith("RCP-")


def test_partial_payment(client, auth_headers):
    """Test partial payment"""
    patient_id, visit_id = create_test_patient_and_visit(client, auth_headers)
    
    # Create invoice for 1000
    invoice_response = client.post(
        "/invoices/",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "items": [{"description": "Treatment", "quantity": 1, "rate": 1000, "amount": 1000}],
            "discount": 0,
            "gst_percent": 0
        },
        headers=auth_headers
    )
    invoice_id = invoice_response.json()["id"]
    
    # Pay 500 first
    client.post(
        "/payments/",
        json={
            "invoice_id": invoice_id,
            "patient_id": patient_id,
            "amount": 500,
            "payment_mode": "cash"
        },
        headers=auth_headers
    )
    
    # Check invoice status
    invoice = client.get(f"/invoices/{invoice_id}", headers=auth_headers).json()
    assert invoice["paid"] == 500
    assert invoice["status"] == "partial"
    
    # Pay remaining 500
    client.post(
        "/payments/",
        json={
            "invoice_id": invoice_id,
            "patient_id": patient_id,
            "amount": 500,
            "payment_mode": "upi"
        },
        headers=auth_headers
    )
    
    # Check invoice is now paid
    invoice = client.get(f"/invoices/{invoice_id}", headers=auth_headers).json()
    assert invoice["paid"] == 1000
    assert invoice["status"] == "paid"


def test_get_pending_invoices(client, auth_headers):
    """Test getting pending invoices"""
    patient_id, visit_id = create_test_patient_and_visit(client, auth_headers)
    
    # Create invoice
    client.post(
        "/invoices/",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "items": [{"description": "Test", "quantity": 1, "rate": 500, "amount": 500}],
            "discount": 0,
            "gst_percent": 0
        },
        headers=auth_headers
    )
    
    response = client.get("/invoices/?status=pending", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(inv["status"] == "pending" for inv in data)
