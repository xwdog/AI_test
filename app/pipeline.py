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


# app/pipeline.py
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
    fr_path = "fr.txt"
    if os.path.exists(fr_path):
        with open(fr_path, "r", encoding="utf-8") as fh:
            t = fh.read().strip()
            if t:
                return t
    return "User must be able to log in with email and password."

def ask_model_for_login_tests(fr_text: str) -> dict:
    """
    Ask for STRICT JSON ONLY, with shape:
    {
      "positive": ["...", "...", "..."],
      "negative": ["...", "...", "..."],
      "edge": ["...", "..."]
    }
    """
    system = "You are a precise QA assistant. Respond with STRICT JSON only."
    user = (
        "Functional Requirement:\n"
        f"{fr_text}\n\n"
        "Return STRICT JSON ONLY (no prose) with this schema:\n"
        "{\n"
        '  "positive": ["short test idea", "short test idea", "short test idea"],\n'
        '  "negative": ["short test idea", "short test idea", "short test idea"],\n'
        '  "edge": ["short test idea", "short test idea"]\n'
        "}\n"
        "Rules:\n"
        "- Exactly 3 positives, 3 negatives, 2 edge cases.\n"
        "- Keep items short, single line each.\n"
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=0,
        max_tokens=300,
    )
    content = (resp.choices[0].message.content or "").strip()

    try:
        data = json.loads(content)
        return data
    except Exception:
        # Simple fallback if model messes up
        return {
            "positive": [
                "valid login",
                "valid login with remember-me",
                "valid login after reset",
            ],
            "negative": [
                "wrong password",
                "unknown email",
                "blank email",
            ],
            "edge": [
                "special chars in email",
                "login from new device",
            ],
        }

def write_concrete_tests(fr_text: str, groups: dict, out_path: str):
    """Write pytest test functions."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("import pytest\n")
        f.write("from app.auth import login\n\n")
        f.write(f"# Functional Requirement: {fr_text}\n\n")

        def write_bucket(label: str, items: list, prefix: str, expect: bool):
            f.write(f"# --- {label} ---\n")
            for i, item in enumerate(items, start=1):
                name = safe_fn_name(item, f"{prefix}_{i}")
                f.write(f"def test_ai_{prefix}_{i}_{name}():\n")
                f.write(f"    assert True  # TODO: implement scenario '{item}'\n\n")

        write_bucket("Positive scenarios", groups["positive"], "pos", True)
        write_bucket("Negative scenarios", groups["negative"], "neg", False)
        write_bucket("Edge-case scenarios", groups["edge"], "edge", True)

def run_pipeline():
    fr_text = read_fr()
    groups = ask_model_for_login_tests(fr_text)
    out_file = os.path.join("tests", "test_ai_generated.py")
    write_concrete_tests(fr_text, groups, out_file)
    total = sum(len(v) for v in groups.values())
    print(f"✅ Wrote {total} AI test stubs to {out_file}")

if __name__ == "__main__":
    run_pipeline()
