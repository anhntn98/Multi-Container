import pytest
import uuid

@pytest.fixture
def test_credentials():
    """Generates unique credentials so tests never clash in the database."""
    uid = uuid.uuid4().hex[:6]
    return {
        "username": f"user_{uid}",
        "email": f"user_{uid}@example.com",
        "password": "SecurePassword123!"
    }

def test_signup_and_login_flow(client, test_credentials):
    # 1. Signup
    signup_res = client.post("/signup", json=test_credentials)
    assert signup_res.status_code == 201, f"Signup failed: {signup_res.text}"

    # 2. Login
    login_payload = {
        "username": test_credentials["username"],
        "password": test_credentials["password"]
    }
    login_res = client.post("/login", json=login_payload)
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    