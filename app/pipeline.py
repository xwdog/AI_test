# touch: verifying file is visible on GitHub

"""
pipeline.py
Orchestrator skeleton:
- loads API key from .env
- sends a functional requirement (FR) to the LLM
- receives test scenarios
- writes pytest stubs into tests/test_ai_generated.py
"""
"""
pipeline.py — baseline:
- loads API key from .env
- sends a functional requirement (FR) to the LLM
- parses scenarios robustly
- writes runnable pytest stubs to tests/test_ai_generated.py
"""
"""
pipeline.py — Step A: structured scenarios
- Reads FR from fr.txt (if present)
- Asks the LLM for JSON with 3 positive, 3 negative, 2 edge cases
- Writes grouped pytest stubs:
    - test_ai_pos_*
    - test_ai_neg_*
    - test_ai_edge_*
"""
"""
pipeline.py — Step B: concrete tests that call app.auth.login
- Reads FR from fr.txt
- Asks the LLM for JSON: 3 positive, 3 negative, 2 edge
  Each item includes a short name, a call {email, password}, and expect (true/false)
- Writes pytest tests that import and CALL login(email=..., password=...) and assert as expected
"""

import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load env & client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def safe_fn_name(text: str, fallback: str) -> str:
    """Make a safe function-name chunk."""
    name = re.sub(r'[^a-zA-Z0-9_]+', '_', text.lower())[:50].strip("_")
    return name or fallback

def read_fr() -> str:
    """Read functional requirement from fr.txt in root, or fall back."""
    fr_path = "fr.txt"
    if os.path.exists(fr_path):
        with open(fr_path, "r", encoding="utf-8") as fh:
            t = fh.read().strip()
            if t:
                print(f"📄 Using FR from {fr_path}: {t[:60]}...")
                return t
            else:
                print(f"⚠️ {fr_path} is empty, falling back to default.")
    else:
        print(f"⚠️ {fr_path} not found, falling back to default.")

    return "User must be able to log in with email and password.  # default"



def ask_model_for_login_tests(fr_text: str) -> dict:
    """
    Ask for STRICT JSON ONLY, with shape:
    {
      "positive": [{"name": "...", "call": {"email":"...","password":"..."},"expect": true}, ... x3],
      "negative": [... x3, expect false],
      "edge":     [... x2, expect true|false]
    }
    RULES:
    - Use known user: alice@example.com / p@ss for at least one positive test.
    - No prose, no markdown, just JSON.
    """
    system = "You are a precise QA assistant. Respond with STRICT JSON only."
    user = (
        "Functional Requirement:\n"
        f"{fr_text}\n\n"
        "Target function signature:\n"
        "from app.auth import login\n"
        "def login(email: str, password: str) -> bool\n\n"
        "Known valid user for positive cases:\n"
        "  email: alice@example.com\n"
        "  password: p@ss\n\n"
        "Return STRICT JSON ONLY (no code blocks, no prose) with this schema:\n"
        "{\n"
        '  "positive": [\n'
        '    {"name": "short_title", "call": {"email":"...","password":"..."}, "expect": true},\n'
        '    {"name": "...",         "call": {"email":"...","password":"..."}, "expect": true},\n'
        '    {"name": "...",         "call": {"email":"...","password":"..."}, "expect": true}\n'
        "  ],\n"
        '  "negative": [\n'
        '    {"name": "...", "call": {"email":"...","password":"..."}, "expect": false},\n'
        '    {"name": "...", "call": {"email":"...","password":"..."}, "expect": false},\n'
        '    {"name": "...", "call": {"email":"...","password":"..."}, "expect": false}\n'
        "  ],\n"
        '  "edge": [\n'
        '    {"name": "...", "call": {"email":"...","password":"..."}, "expect": true},\n'
        '    {"name": "...", "call": {"email":"...","password":"..."}, "expect": false}\n'
        "  ]\n"
        "}\n"
        "Rules:\n"
        "- Keep names short.\n"
        "- No line breaks in names.\n"
        "- Exactly 3/3/2 items.\n"
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=0,
        max_tokens=500,
    )
    content = (resp.choices[0].message.content or "").strip()

    # Parse JSON or fallback
    try:
        data = json.loads(content)
        for k in ("positive","negative","edge"):
            data[k] = list(data.get(k, []))
        return data
    except Exception:
        # Minimal safe fallback if model ignored JSON
        return {
            "positive": [
                {"name":"valid_login", "call":{"email":"alice@example.com","password":"p@ss"}, "expect": True},
                {"name":"valid_login_again", "call":{"email":"alice@example.com","password":"p@ss"}, "expect": True},
                {"name":"valid_login_repeat", "call":{"email":"alice@example.com","password":"p@ss"}, "expect": True},
            ],
            "negative": [
                {"name":"wrong_password", "call":{"email":"alice@example.com","password":"nope"}, "expect": False},
                {"name":"unknown_user",   "call":{"email":"bob@example.com","password":"p@ss"},   "expect": False},
                {"name":"blank_email",    "call":{"email":"","password":"p@ss"},                 "expect": False},
            ],
            "edge": [
                {"name":"special_chars_email", "call":{"email":"ali+ce@example.com","password":"p@ss"}, "expect": False},
                {"name":"empty_password",      "call":{"email":"alice@example.com","password":""},      "expect": False},
            ],
        }

def normalize_counts(groups: dict) -> dict:
    """Force exactly 3/3/2 items (truncate/pad)."""
    def fit(lst, target, pads):
        lst = [x for x in lst if isinstance(x, dict)][:target]
        while len(lst) < target:
            lst.append(pads[len(lst)])
        return lst

    pads_pos = [
        {"name":"valid_login_pad1","call":{"email":"alice@example.com","password":"p@ss"},"expect":True},
        {"name":"valid_login_pad2","call":{"email":"alice@example.com","password":"p@ss"},"expect":True},
        {"name":"valid_login_pad3","call":{"email":"alice@example.com","password":"p@ss"},"expect":True},
    ]
    pads_neg = [
        {"name":"wrong_password_pad","call":{"email":"alice@example.com","password":"nope"},"expect":False},
        {"name":"unknown_user_pad",  "call":{"email":"nobody@example.com","password":"p@ss"},"expect":False},
        {"name":"blank_email_pad",   "call":{"email":"","password":"p@ss"},"expect":False},
    ]
    pads_edge = [
        {"name":"special_chars_pad","call":{"email":"ali+ce@example.com","password":"p@ss"},"expect":False},
        {"name":"empty_password_pad","call":{"email":"alice@example.com","password":""},"expect":False},
    ]

    groups["positive"] = fit(groups.get("positive", []), 3, pads_pos)
    groups["negative"] = fit(groups.get("negative", []), 3, pads_neg)
    groups["edge"]     = fit(groups.get("edge", []),     2, pads_edge)
    return groups

def write_concrete_tests(fr_text: str, groups: dict, out_path: str):
    """Generate pytest that IMPORTS and CALLS login()."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("import pytest\n")
        f.write("from app.auth import login\n\n")
        f.write(f"# Functional Requirement: {fr_text}\n\n")

        def write_bucket(label: str, items: list, prefix: str):
            f.write(f"# --- {label} ---\n")
            for i, item in enumerate(items, start=1):
                name = safe_fn_name(item.get("name","case"), f"{prefix}_{i}")
                call = item.get("call", {})
                email = call.get("email","")
                password = call.get("password","")
                expect = item.get("expect", True)
                expect_kw = "True" if expect else "False"
                f.write(f"def test_ai_{prefix}_{i}_{name}():\n")
                f.write(f"    result = login(email={email!r}, password={password!r})\n")
                f.write(f"    assert result is {expect_kw}\n\n")

        write_bucket("Positive scenarios", groups["positive"], "pos")
        write_bucket("Negative scenarios", groups["negative"], "neg")
        write_bucket("Edge-case scenarios", groups["edge"], "edge")

def run_pipeline():
    fr_text = read_fr()
    groups = ask_model_for_login_tests(fr_text)
    groups = normalize_counts(groups)
    out_file = os.path.join("tests", "test_ai_generated.py")
    write_concrete_tests(fr_text, groups, out_file)
    total = sum(len(v) for v in groups.values())
    print(f"✅ Wrote {total} concrete tests to {out_file}")

if __name__ == "__main__":
    run_pipeline()

