
# tests/test_api_example.py
# -----------------------------------------------------------------------------
# This file contains tests for our FastAPI application (app/api.py).
#
# We use FastAPI's TestClient to "pretend" to call the API endpoints in memory.
# No server (Uvicorn) is started here — everything runs inside pytest.
#
# Strategy:
#   - Import the FastAPI instance (my_api) from app/api.py
#   - Use TestClient to simulate GET requests to our endpoints
#   - Assert that the responses are what we expect (status code + JSON)
# -----------------------------------------------------------------------------

from fastapi.testclient import TestClient
from app.api import my_api

# -----------------------------------------------------------------------------
# Create a test client
# -----------------------------------------------------------------------------
# TestClient wraps around our FastAPI instance (my_api).
# With this, we can "call" endpoints as if we were a browser or API client.
# -----------------------------------------------------------------------------
client = TestClient(my_api)

# -----------------------------------------------------------------------------
# Test: Root endpoint
# -----------------------------------------------------------------------------
# Visiting "/" should return a simple JSON message.
# -----------------------------------------------------------------------------
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

# -----------------------------------------------------------------------------
# Test: Login endpoint (success)
# -----------------------------------------------------------------------------
# Alice exists in app/auth.py with password "p@ss".
# If we send those credentials, we should get {"ok": True}.
# -----------------------------------------------------------------------------
def test_login_success():
    response = client.get("/login", params={"email": "alice@example.com", "password": "p@ss"})
    assert response.status_code == 200
    assert response.json() == {"ok": True}

# -----------------------------------------------------------------------------
# Test: Login endpoint (wrong password)
# -----------------------------------------------------------------------------
# Alice exists, but if we give the wrong password, we expect {"ok": False}.
# -----------------------------------------------------------------------------
def test_login_wrong_password():
    response = client.get("/login", params={"email": "alice@example.com", "password": "wrong"})
    assert response.status_code == 200
    assert response.json() == {"ok": False}
