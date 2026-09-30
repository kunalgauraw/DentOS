"""AUTH-001: every endpoint except login must require a valid token"""
import pytest

PROTECTED = [
    ("get", "/patients/"),
    ("post", "/patients/"),
    ("get", "/patients/1"),
    ("put", "/patients/1"),
    ("delete", "/patients/1"),
    ("get", "/visits/"),
    ("post", "/visits/"),
    ("put", "/visits/1"),
    ("get", "/prescriptions/"),
    ("post", "/prescriptions/"),
    ("get", "/invoices/"),
    ("post", "/invoices/"),
    ("get", "/payments/"),
    ("post", "/payments/"),
    ("get", "/payments/today-collection"),
    ("get", "/dashboard/stats"),
    ("get", "/dashboard/recent-patients"),
    ("get", "/dashboard/pending-payments"),
    ("get", "/auth/me"),
]


def _call(client, method, path, headers=None):
    return client.request(method.upper(), path, json={} if method in ("post", "put") else None, headers=headers)


@pytest.mark.parametrize("method,path", PROTECTED)
def test_requires_token(client, method, path):
    response = _call(client, method, path)
    assert response.status_code == 401, f"{method.upper()} {path} -> {response.status_code}"


@pytest.mark.parametrize("method,path", PROTECTED)
def test_rejects_garbage_token(client, method, path):
    response = _call(client, method, path, headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401, f"{method.upper()} {path} -> {response.status_code}"


def test_public_endpoints_open(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200


def test_disabled_user_cannot_use_token(client, db, auth_headers):
    from app.models import User
    user = db.query(User).filter(User.username == "testadmin").first()
    user.is_active = False
    db.commit()

    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 401
