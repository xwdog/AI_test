import pytest
from app.auth import login

# Functional Requirement: User must be able to log in with email and password.

# --- Positive scenarios ---
def test_ai_pos_1_valid_user():
    result = login(email='alice@example.com', password='p@ss')
    assert result is True

def test_ai_pos_2_valid_user_upper():
    result = login(email='ALICE@EXAMPLE.COM', password='p@ss')
    assert result is True

def test_ai_pos_3_valid_user_space():
    result = login(email=' alice@example.com ', password=' p@ss ')
    assert result is True

# --- Negative scenarios ---
def test_ai_neg_1_invalid_email():
    result = login(email='bob@example.com', password='p@ss')
    assert result is False

def test_ai_neg_2_invalid_password():
    result = login(email='alice@example.com', password='wrong')
    assert result is False

def test_ai_neg_3_empty_credentials():
    result = login(email='', password='')
    assert result is False

# --- Edge-case scenarios ---
def test_ai_edge_1_email_missing_at():
    result = login(email='aliceexample.com', password='p@ss')
    assert result is False

def test_ai_edge_2_password_empty():
    result = login(email='alice@example.com', password='')
    assert result is False

