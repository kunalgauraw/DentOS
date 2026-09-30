"""Tests for visit/consultation endpoints"""
from datetime import datetime, timedelta, timezone


def create_visit(client, headers, patient_id, **overrides):
    payload = {"patient_id": patient_id, "chief_complaint": "Tooth pain"}
    payload.update(overrides)
    return client.post("/visits/", json=payload, headers=headers)


def test_create_visit(client, auth_headers, patient):
    response = create_visit(client, auth_headers, patient["id"], bp="120/80", blood_sugar="90")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == patient["id"]
    assert data["chief_complaint"] == "Tooth pain"
    assert data["visit_id"].startswith("VIS-")
    assert data["status"] == "completed"


def test_visit_captures_dentist_from_session(client, auth_headers, patient):
    """VIS-004: doctor_id comes from the logged-in dentist/admin"""
    me = client.get("/auth/me", headers=auth_headers).json()
    response = create_visit(client, auth_headers, patient["id"])
    assert response.json()["doctor_id"] == me["id"]


def test_visit_by_receptionist_has_no_doctor(client, receptionist_headers, patient):
    """A receptionist is not a dentist, so doctor_id stays empty unless provided"""
    response = create_visit(client, receptionist_headers, patient["id"])
    assert response.status_code == 200
    assert response.json()["doctor_id"] is None


def test_create_visit_minimal(client, auth_headers, patient):
    response = client.post("/visits/", json={"patient_id": patient["id"]}, headers=auth_headers)
    assert response.status_code == 200


def test_create_visit_invalid_patient(client, auth_headers):
    response = create_visit(client, auth_headers, 99999)
    assert response.status_code == 404


def test_get_visits_for_patient(client, auth_headers, patient):
    create_visit(client, auth_headers, patient["id"], chief_complaint="Visit 1")
    create_visit(client, auth_headers, patient["id"], chief_complaint="Visit 2")

    response = client.get(f"/visits/?patient_id={patient['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_visit_with_followup(client, auth_headers, patient):
    response = create_visit(
        client, auth_headers, patient["id"],
        chief_complaint="Root canal", follow_up_date="2026-10-15", follow_up_reason="Check healing",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["follow_up_date"] == "2026-10-15"
    assert data["follow_up_reason"] == "Check healing"


def test_update_visit_same_day(client, receptionist_headers, patient):
    """VIS-006: same-day edits allowed for any user"""
    visit_id = create_visit(client, receptionist_headers, patient["id"]).json()["id"]
    response = client.put(f"/visits/{visit_id}", json={"advice": "Rinse twice daily"}, headers=receptionist_headers)
    assert response.status_code == 200
    assert response.json()["advice"] == "Rinse twice daily"


def test_update_old_visit_forbidden_for_non_admin(client, db, auth_headers, receptionist_headers, patient):
    """VIS-007: after the day, only admin can edit"""
    from app.models import Visit
    visit_id = create_visit(client, auth_headers, patient["id"]).json()["id"]
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    visit.visit_date = datetime.now(timezone.utc) - timedelta(days=2)
    db.commit()

    denied = client.put(f"/visits/{visit_id}", json={"advice": "late edit"}, headers=receptionist_headers)
    assert denied.status_code == 403

    allowed = client.put(f"/visits/{visit_id}", json={"advice": "admin edit"}, headers=auth_headers)
    assert allowed.status_code == 200
    assert allowed.json()["advice"] == "admin edit"
