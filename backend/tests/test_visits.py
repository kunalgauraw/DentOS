"""Tests for visit/consultation endpoints"""


def create_test_patient(client, auth_headers):
    """Helper to create a test patient"""
    response = client.post(
        "/patients/",
        json={"full_name": "Visit Test Patient", "mobile": "9876500001", "gender": "Male"},
        headers=auth_headers
    )
    return response.json()["id"]


def test_create_visit(client, auth_headers):
    """Test creating a new visit"""
    patient_id = create_test_patient(client, auth_headers)
    
    response = client.post(
        "/visits/",
        json={
            "patient_id": patient_id,
            "chief_complaint": "Tooth pain",
            "bp": "120/80",
            "blood_sugar": "90"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == patient_id
    assert data["chief_complaint"] == "Tooth pain"
    assert data["visit_id"].startswith("VIS-")
    assert data["status"] == "completed"


def test_create_visit_minimal(client, auth_headers):
    """Test creating visit with minimal data"""
    patient_id = create_test_patient(client, auth_headers)
    
    response = client.post(
        "/visits/",
        json={"patient_id": patient_id},
        headers=auth_headers
    )
    assert response.status_code == 200


def test_create_visit_invalid_patient(client, auth_headers):
    """Test creating visit for non-existent patient"""
    response = client.post(
        "/visits/",
        json={"patient_id": 99999, "chief_complaint": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 404


def test_get_visits_for_patient(client, auth_headers):
    """Test getting visits for a specific patient"""
    patient_id = create_test_patient(client, auth_headers)
    
    # Create multiple visits
    client.post(
        "/visits/",
        json={"patient_id": patient_id, "chief_complaint": "Visit 1"},
        headers=auth_headers
    )
    client.post(
        "/visits/",
        json={"patient_id": patient_id, "chief_complaint": "Visit 2"},
        headers=auth_headers
    )
    
    response = client.get(f"/visits/?patient_id={patient_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_visit_with_followup(client, auth_headers):
    """Test creating visit with follow-up date"""
    patient_id = create_test_patient(client, auth_headers)
    
    response = client.post(
        "/visits/",
        json={
            "patient_id": patient_id,
            "chief_complaint": "Root canal",
            "follow_up_date": "2026-10-15",
            "follow_up_reason": "Check healing"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["follow_up_date"] == "2026-10-15"
    assert data["follow_up_reason"] == "Check healing"
