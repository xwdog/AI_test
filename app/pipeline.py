# touch: verifying file is visible on GitHub

"""
pipeline.py
Orchestrator skeleton:
- will read a Functional Requirement (FR)
- will call the LLM to propose scenarios
- will generate pytest tests into tests/
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def run_pipeline():
    # 1) Load env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("❌ No API key found. Check your .env file.")
        return

    client = OpenAI(api_key=api_key)

    # 2) Hardcoded Functional Requirement (FR) for now
    fr_text = "User must be able to log in with email and password."

    # 3) Ask AI to generate test scenarios
    prompt = f"""
    Functional Requirement: {fr_text}

    Please generate:
    - 3 positive test scenarios
    - 2 negative test scenarios
    - 1 edge-case scenario

    Output format:
    Plain text bullet points.
    """

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a QA assistant that generates test scenarios."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0
    )

    scenarios = resp.choices[0].message.content.strip()

    # 4) Write results to tests/test_ai_generated.py (as comments for now)
    out_file = os.path.join("tests", "test_ai_generated.py")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# AI-generated test scenarios\n")
        f.write("# Functional Requirement: " + fr_text + "\n\n")
        for line in scenarios.splitlines():
            f.write("# " + line + "\n")

    print(f"✅ Test scenarios written to {out_file}")
    print("Preview:\n", scenarios)

if __name__ == "__main__":
    run_pipeline()





