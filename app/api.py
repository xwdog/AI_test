
# app/api.py
# -----------------------------------------------------------------------------
# This file defines the API endpoints that wrap around your login logic.
# It uses FastAPI to expose functions (like login) as HTTP endpoints.
# -----------------------------------------------------------------------------

from fastapi import FastAPI
from app.auth import login

# -----------------------------------------------------------------------------
# Create FastAPI instance
# -----------------------------------------------------------------------------
# FastAPI is a class. Calling FastAPI() creates an *object* (an instance).
# We name it "my_api" (instead of just "app") so it's clear what it is:
#    - This object will hold all the endpoints we define below.
#    - Uvicorn or TestClient will "talk" to this object to run our API.
# -----------------------------------------------------------------------------
my_api = FastAPI()

# -----------------------------------------------------------------------------
# Root endpoint ("/")
# -----------------------------------------------------------------------------
# When someone visits http://127.0.0.1:8000/, this function runs.
# It simply returns a JSON message that confirms the API is running.
# -----------------------------------------------------------------------------
@my_api.get("/")
def root():
    return {"message": "API is running"}

# -----------------------------------------------------------------------------
# Login endpoint ("/login")
# -----------------------------------------------------------------------------
# Example:
#   http://127.0.0.1:8000/login?email=alice@example.com&password=p@ss
#
# The "email" and "password" in the URL become parameters to this function.
# We pass them to our login() function (from app/auth.py).
# The result (True/False) is wrapped into JSON {"ok": ...}.
# -----------------------------------------------------------------------------
@my_api.get("/login")
def login_endpoint(email: str, password: str):
    return {"ok": login(email, password)}
