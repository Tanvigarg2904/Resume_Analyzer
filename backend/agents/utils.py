import re
import json

def extract_json(text):

    match = re.search(r"\{.*\}", text, re.S)

    if not match:
        raise ValueError("No JSON found")

    raw = match.group()

    # Fix single quotes → double quotes
    raw = raw.replace("'", '"')

    # Remove trailing commas
    raw = re.sub(r",\s*}", "}", raw)
    raw = re.sub(r",\s*]", "]", raw)

    return json.loads(raw)

