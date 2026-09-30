"""Tests for patient endpoints"""
from datetime import date


def make_patient(client, headers, **overrides):
    payload = {"full_name": "Test Patient", "mobile": "9876543210", "gender": "Male", "age": 30}
    payload.update(overrides)
    return client.post("/patients/", json=payload, headers=headers)


def test_create_patient(client, auth_headers):
    response = make_patient(client, auth_headers, full_name="John Doe", age=35)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["mobile"] == "9876543210"
    assert data["gender"] == "male"
    assert data["patient_id"].startswith("PAT-")


def test_create_patient_with_dob_derives_age(client, auth_headers):
    """PAT-005/006: DOB alone is acceptable and age is derived"""
    dob = date(date.today().year - 40, 1, 1).isoformat()
    response = make_patient(client, auth_headers, age=None, date_of_birth=dob)
    assert response.status_code == 200
    assert response.json()["age"] in (39, 40)


def test_create_patient_requires_age_or_dob(client, auth_headers):
    """PAT-006"""
    response = make_patient(client, auth_headers, age=None)
    assert response.status_code == 422
    assert "age or date of birth" in response.text.lower()


def test_create_patient_invalid_mobile(client, auth_headers):
    """PAT-003: mobile must be exactly 10 digits"""
    for bad in ["12345", "98765432101", "abcdefghij"]:
        response = make_patient(client, auth_headers, mobile=bad)
        assert response.status_code == 422, bad


def test_create_patient_mobile_is_normalised(client, auth_headers):
    response = make_patient(client, auth_headers, mobile="98765-43210")
    assert response.status_code == 200
    assert response.json()["mobile"] == "9876543210"


def test_create_patient_short_name_rejected(client, auth_headers):
    response = make_patient(client, auth_headers, full_name="A")
    assert response.status_code == 422


def test_duplicate_mobile_allowed_with_warning(client, auth_headers):
    """PAT-004: shared mobile is allowed (families); check-mobile lets the UI warn"""
    assert make_patient(client, auth_headers, full_name="Patient 1", mobile="9876543212").status_code == 200
    assert make_patient(client, auth_headers, full_name="Patient 2", mobile="9876543212").status_code == 200

    response = client.get("/patients/check-mobile?mobile=9876543212", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_patients(client, auth_headers):
    make_patient(client, auth_headers, mobile="9876543213")
    response = client.get("/patients/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_patient_by_id(client, auth_headers):
    patient_id = make_patient(client, auth_headers, full_name="Specific Patient", mobile="9876543214").json()["id"]
    response = client.get(f"/patients/{patient_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Specific Patient"


def test_get_nonexistent_patient(client, auth_headers):
    response = client.get("/patients/99999", headers=auth_headers)
    assert response.status_code == 404


def test_search_patients(client, auth_headers):
    make_patient(client, auth_headers, full_name="Rahul Kumar", mobile="9876543215")
    make_patient(client, auth_headers, full_name="Priya Singh", mobile="9876543216")

    response = client.get("/patients/?search=Rahul", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Rahul Kumar"


def test_update_patient(client, auth_headers):
    patient_id = make_patient(client, auth_headers, mobile="9876543217").json()["id"]
    response = client.put(
        f"/patients/{patient_id}",
        json={"blood_group": "O+", "allergies": "Penicillin"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["blood_group"] == "O+"
    assert response.json()["allergies"] == "Penicillin"


def test_update_patient_invalid_mobile(client, auth_headers):
    patient_id = make_patient(client, auth_headers, mobile="9876543217").json()["id"]
    response = client.put(f"/patients/{patient_id}", json={"mobile": "123"}, headers=auth_headers)
    assert response.status_code == 422


def test_delete_patient_as_admin(client, auth_headers):
    patient_id = make_patient(client, auth_headers, mobile="9876543218").json()["id"]
    response = client.delete(f"/patients/{patient_id}", headers=auth_headers)
    assert response.status_code == 200
    assert client.get(f"/patients/{patient_id}", headers=auth_headers).status_code == 404


def test_delete_patient_as_receptionist_forbidden(client, auth_headers, receptionist_headers):
    patient_id = make_patient(client, auth_headers, mobile="9876543219").json()["id"]
    response = client.delete(f"/patients/{patient_id}", headers=receptionist_headers)
    assert response.status_code == 403
    # still there
    assert client.get(f"/patients/{patient_id}", headers=auth_headers).status_code == 200
