# app/auth.py
USERS = {
    "alice@example.com": "p@ss",
    "bob@example.com": "hunter2",  # new user
    "carol@example.com": "letmein"  # another user
}

def login(email: str, password: str) -> bool:
    # normalize email & password
    email = email.strip().lower()
    password = password.strip()
    return USERS.get(email) == password


