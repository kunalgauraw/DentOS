"""Tests for authentication endpoints"""


def test_login_success(client):
    """Test successful login"""
    response = client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Test login with wrong password"""
    response = client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect" in response.json()["detail"] or "Invalid" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "anypassword"}
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testadmin"
    assert data["full_name"] == "Test Admin"


def test_get_current_user_no_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get("/auth/me")
    assert response.status_code == 401
