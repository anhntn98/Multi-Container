import pytest
import httpx
import time

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def client():
    """Shared HTTP client pointing to your gateway."""
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        yield client



@pytest.fixture(scope="session", autouse=True)
def verify_url_is_up(client):
    """
    Retries connecting to the main URL to allow backend services 
    time to fully initialize inside Docker.
    """
    max_retries = 15
    delay_seconds = 2

    for attempt in range(1, max_retries + 1):
        try:
            response = client.get("/")
            if response.status_code == 200:
                print(f"\n✅ Target URL responded with 200 OK on attempt {attempt}!")
                return
            print(f"⏳ Attempt {attempt}/{max_retries}: Got HTTP {response.status_code}, retrying...")
        except httpx.RequestError as e:
            print(f"⏳ Attempt {attempt}/{max_retries}: Connection failed ({e}), retrying...")

        time.sleep(delay_seconds)

    pytest.fail("❌ Target URL failed to return 200 OK within the timeout period (502/down).")