import pytest
from app.auth import login

# Functional Requirement: System must allow multiple registered users (Alice, Bob, Carol) to log in with their email + password.

# --- Positive scenarios ---
def test_ai_pos_1_alice_logs_in_with_correct_email_and_password():
    assert True  # TODO: implement scenario 'Alice logs in with correct email and password'

def test_ai_pos_2_bob_logs_in_with_correct_email_and_password():
    assert True  # TODO: implement scenario 'Bob logs in with correct email and password'

def test_ai_pos_3_carol_logs_in_with_correct_email_and_password():
    assert True  # TODO: implement scenario 'Carol logs in with correct email and password'

# --- Negative scenarios ---
def test_ai_neg_1_alice_logs_in_with_incorrect_password():
    assert True  # TODO: implement scenario 'Alice logs in with incorrect password'

def test_ai_neg_2_bob_logs_in_with_unregistered_email():
    assert True  # TODO: implement scenario 'Bob logs in with unregistered email'

def test_ai_neg_3_carol_logs_in_with_empty_email_field():
    assert True  # TODO: implement scenario 'Carol logs in with empty email field'

# --- Edge-case scenarios ---
def test_ai_edge_1_alice_logs_in_with_maximum_length_email():
    assert True  # TODO: implement scenario 'Alice logs in with maximum length email'

def test_ai_edge_2_bob_logs_in_with_special_characters_in_password():
    assert True  # TODO: implement scenario 'Bob logs in with special characters in password'

