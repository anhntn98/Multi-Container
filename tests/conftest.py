import pytest
import httpx

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def client():
    """Shared HTTP client pointing to your gateway."""
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        yield client



@pytest.fixture(scope="session", autouse=True)
def verify_url_is_up(client):
    """Verifies the root URL is reachable before running any tests."""
    try:
        response = client.get("/")
        assert response.status_code == 200, f"URL returned status code {response.status_code}"
        print("\n✅ Main URL is reachable! Executing test suite...")
    except Exception as e:
        pytest.fail(f"❌ Target URL is not reachable: {e}")