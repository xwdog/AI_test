from app.auth import login

def test_login_success():
    assert login("alice@example.com", "p@ss") is True

def test_login_wrong_password():
    assert login("alice@example.com", "nope") is False
