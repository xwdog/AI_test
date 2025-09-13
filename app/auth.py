# app/auth.py
# Store emails in lowercase (canonical form)
USERS = {"alice@example.com": "p@ss"}

def login(email: str, password: str) -> bool:
    # Guard against None
    if email is None or password is None:
        return False

    # Normalize inputs:
    # - Emails are case-insensitive and users may add spaces
    # - Passwords are case-sensitive but may have accidental spaces
    email_norm = email.strip().lower()
    password_norm = password.strip()

    return USERS.get(email_norm) == password_norm

