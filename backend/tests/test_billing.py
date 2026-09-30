"""Tests for billing (invoices and payments) endpoints"""
import pytest


@pytest.fixture
def visit(client, auth_headers, patient):
    response = client.post(
        "/visits/", json={"patient_id": patient["id"], "chief_complaint": "Billing test"}, headers=auth_headers
    )
    return response.json()


def item(description="Treatment", rate=1000, quantity=1):
    return {"description": description, "quantity": quantity, "rate": rate, "amount": rate * quantity}


def create_invoice(client, headers, patient_id, visit_id=None, items=None, **overrides):
    payload = {
        "patient_id": patient_id,
        "visit_id": visit_id,
        "items": items if items is not None else [item()],
        "discount": 0,
        "gst_percent": 0,
    }
    payload.update(overrides)
    return client.post("/invoices/", json=payload, headers=headers)


def pay(client, headers, invoice_id, patient_id, amount, mode="cash", **overrides):
    payload = {"invoice_id": invoice_id, "patient_id": patient_id, "amount": amount, "payment_mode": mode}
    payload.update(overrides)
    return client.post("/payments/", json=payload, headers=headers)


# ---- Invoices -------------------------------------------------------------

def test_create_invoice(client, auth_headers, patient, visit):
    response = create_invoice(
        client, auth_headers, patient["id"], visit["id"],
        items=[item("Consultation", 500), item("X-Ray", 300)], discount=50,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 800
    assert data["discount"] == 50
    assert data["total"] == 750
    assert data["status"] == "pending"
    assert data["invoice_id"].startswith("INV-")
    assert data["visit_id"] == visit["id"]


def test_invoice_attributed_to_visit_doctor(client, auth_headers, patient, visit):
    response = create_invoice(client, auth_headers, patient["id"], visit["id"])
    assert response.json()["doctor_id"] == visit["doctor_id"]


def test_create_invoice_with_gst(client, auth_headers, patient, visit):
    response = create_invoice(client, auth_headers, patient["id"], visit["id"], items=[item(rate=1000)], gst_percent=18)
    assert response.status_code == 200
    data = response.json()
    assert data["gst_amount"] == 180
    assert data["total"] == 1180


def test_invoice_requires_items(client, auth_headers, patient):
    """INV-002"""
    assert create_invoice(client, auth_headers, patient["id"], items=[]).status_code == 422


def test_invoice_rejects_zero_amount_item(client, auth_headers, patient):
    """INV-003"""
    assert create_invoice(client, auth_headers, patient["id"], items=[item(rate=0)]).status_code == 422


def test_invoice_rejects_negative_rate(client, auth_headers, patient):
    assert create_invoice(client, auth_headers, patient["id"], items=[item(rate=-100)]).status_code == 422


def test_invoice_server_recomputes_line_amount(client, auth_headers, patient):
    """Client-supplied amount is ignored; qty * rate is the truth"""
    tampered = {"description": "Crown", "quantity": 2, "rate": 500, "amount": 1}
    response = create_invoice(client, auth_headers, patient["id"], items=[tampered])
    assert response.status_code == 200
    assert response.json()["subtotal"] == 1000


def test_invoice_discount_cannot_exceed_subtotal(client, auth_headers, patient):
    """INV-004"""
    response = create_invoice(client, auth_headers, patient["id"], items=[item(rate=500)], discount=600)
    assert response.status_code == 422


def test_invoice_visit_must_belong_to_patient(client, auth_headers, patient, visit):
    other = client.post(
        "/patients/", json={"full_name": "Other", "mobile": "9000000002", "gender": "male", "age": 40},
        headers=auth_headers,
    ).json()
    response = create_invoice(client, auth_headers, other["id"], visit["id"])
    assert response.status_code == 400


def test_get_pending_invoices(client, auth_headers, patient, visit):
    create_invoice(client, auth_headers, patient["id"], visit["id"], items=[item(rate=500)])
    response = client.get("/invoices/?status=pending", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(inv["status"] == "pending" for inv in data)
    assert data[0]["patient_name"] == patient["full_name"]


def test_filter_invoices_by_visit(client, auth_headers, patient, visit):
    create_invoice(client, auth_headers, patient["id"], visit["id"])
    response = client.get(f"/invoices/?visit_id={visit['id']}", headers=auth_headers)
    assert len(response.json()) == 1


# ---- Payments -------------------------------------------------------------

def test_collect_payment(client, auth_headers, patient, visit):
    invoice_id = create_invoice(client, auth_headers, patient["id"], visit["id"]).json()["id"]
    me = client.get("/auth/me", headers=auth_headers).json()

    response = pay(client, auth_headers, invoice_id, patient["id"], 1000)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 1000
    assert data["payment_mode"] == "cash"
    assert data["receipt_id"].startswith("RCP-")
    assert data["received_by"] == me["id"]


def test_partial_payment(client, auth_headers, patient, visit):
    invoice_id = create_invoice(client, auth_headers, patient["id"], visit["id"]).json()["id"]

    pay(client, auth_headers, invoice_id, patient["id"], 500)
    invoice = client.get(f"/invoices/{invoice_id}", headers=auth_headers).json()
    assert invoice["paid"] == 500
    assert invoice["balance"] == 500
    assert invoice["status"] == "partial"

    pay(client, auth_headers, invoice_id, patient["id"], 500, mode="upi", reference_no="UPI123")
    invoice = client.get(f"/invoices/{invoice_id}", headers=auth_headers).json()
    assert invoice["paid"] == 1000
    assert invoice["balance"] == 0
    assert invoice["status"] == "paid"


def test_payment_cannot_exceed_balance(client, auth_headers, patient, visit):
    """PAY-003"""
    invoice_id = create_invoice(client, auth_headers, patient["id"], visit["id"]).json()["id"]
    response = pay(client, auth_headers, invoice_id, patient["id"], 1500)
    assert response.status_code == 400


def test_payment_must_be_positive(client, auth_headers, patient, visit):
    """PAY-002"""
    invoice_id = create_invoice(client, auth_headers, patient["id"], visit["id"]).json()["id"]
    assert pay(client, auth_headers, invoice_id, patient["id"], 0).status_code == 400
    assert pay(client, auth_headers, invoice_id, patient["id"], -5).status_code == 400


def test_non_cash_payment_requires_reference(client, auth_headers, patient, visit):
    """PAY-005"""
    invoice_id = create_invoice(client, auth_headers, patient["id"], visit["id"]).json()["id"]
    assert pay(client, auth_headers, invoice_id, patient["id"], 100, mode="upi").status_code == 400
    assert pay(client, auth_headers, invoice_id, patient["id"], 100, mode="card", reference_no="").status_code == 400
    assert pay(client, auth_headers, invoice_id, patient["id"], 100, mode="upi", reference_no="TXN1").status_code == 200


def test_payment_invoice_must_belong_to_patient(client, auth_headers, patient, visit):
    invoice_id = create_invoice(client, auth_headers, patient["id"], visit["id"]).json()["id"]
    other = client.post(
        "/patients/", json={"full_name": "Other", "mobile": "9000000003", "gender": "male", "age": 40},
        headers=auth_headers,
    ).json()
    assert pay(client, auth_headers, invoice_id, other["id"], 100).status_code == 400
