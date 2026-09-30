"""Tests for patient endpoints"""


def test_create_patient(client, auth_headers):
    """Test creating a new patient"""
    response = client.post(
        "/patients/",
        json={
            "full_name": "John Doe",
            "mobile": "9876543210",
            "gender": "Male",
            "age": 35
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["mobile"] == "9876543210"
    assert data["patient_id"].startswith("PAT-")


def test_create_patient_minimal(client, auth_headers):
    """Test creating patient with minimal required fields"""
    response = client.post(
        "/patients/",
        json={
            "full_name": "Jane Doe",
            "mobile": "9876543211",
            "gender": "Female"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["age"] is None


def test_create_patient_duplicate_mobile(client, auth_headers):
    """Test that duplicate mobile numbers are rejected"""
    # Create first patient
    client.post(
        "/patients/",
        json={"full_name": "Patient 1", "mobile": "9876543212", "gender": "Male"},
        headers=auth_headers
    )
    
    # Try to create second patient with same mobile
    response = client.post(
        "/patients/",
        json={"full_name": "Patient 2", "mobile": "9876543212", "gender": "Female"},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_get_patients(client, auth_headers):
    """Test getting list of patients"""
    # Create a patient first
    client.post(
        "/patients/",
        json={"full_name": "Test Patient", "mobile": "9876543213", "gender": "Male"},
        headers=auth_headers
    )
    
    response = client.get("/patients/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_patient_by_id(client, auth_headers):
    """Test getting a specific patient"""
    # Create a patient
    create_response = client.post(
        "/patients/",
        json={"full_name": "Specific Patient", "mobile": "9876543214", "gender": "Female"},
        headers=auth_headers
    )
    patient_id = create_response.json()["id"]
    
    # Get the patient
    response = client.get(f"/patients/{patient_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Specific Patient"


def test_get_nonexistent_patient(client, auth_headers):
    """Test getting a patient that doesn't exist"""
    response = client.get("/patients/99999", headers=auth_headers)
    assert response.status_code == 404


def test_search_patients(client, auth_headers):
    """Test searching patients by name"""
    # Create patients
    client.post(
        "/patients/",
        json={"full_name": "Rahul Kumar", "mobile": "9876543215", "gender": "Male"},
        headers=auth_headers
    )
    client.post(
        "/patients/",
        json={"full_name": "Priya Singh", "mobile": "9876543216", "gender": "Female"},
        headers=auth_headers
    )
    
    # Search for Rahul
    response = client.get("/patients/?search=Rahul", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Rahul Kumar"


def test_update_patient(client, auth_headers):
    """Test updating a patient"""
    # Create a patient
    create_response = client.post(
        "/patients/",
        json={"full_name": "Update Test", "mobile": "9876543217", "gender": "Male"},
        headers=auth_headers
    )
    patient_id = create_response.json()["id"]
    
    # Update the patient
    response = client.put(
        f"/patients/{patient_id}",
        json={"blood_group": "O+", "allergies": "Penicillin"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["blood_group"] == "O+"
    assert response.json()["allergies"] == "Penicillin"


def test_delete_patient(client, auth_headers):
    """Test deleting a patient"""
    # Create a patient
    create_response = client.post(
        "/patients/",
        json={"full_name": "Delete Test", "mobile": "9876543218", "gender": "Male"},
        headers=auth_headers
    )
    patient_id = create_response.json()["id"]
    
    # Delete the patient
    response = client.delete(f"/patients/{patient_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify patient is deleted
    get_response = client.get(f"/patients/{patient_id}", headers=auth_headers)
    assert get_response.status_code == 404
