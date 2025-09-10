import os
from dotenv import load_dotenv

# Load the .env file so its values become environment variables
load_dotenv()

# Grab the variables
key = os.getenv("OPENAI_API_KEY", "")
model = os.getenv("OPENAI_MODEL", "")

# Mask the key so we don’t print the whole secret
def mask(s): 
    return s[:4] + "..." + s[-4:] if len(s) > 8 else "(not set)"

# Print results
print("OPENAI_API_KEY:", mask(key))
print("OPENAI_MODEL:", model or "(not set)")