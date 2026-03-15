import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ------------------------------------------------------
# JSON cleaner (prevents parsing failures)
# ------------------------------------------------------
def clean_json(raw):

    raw = raw.strip()

    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object detected")

    return raw[start:end+1]


# ------------------------------------------------------
# Role Agent
# ------------------------------------------------------
def role_agent(role):

    prompt = f"""
You are a senior technical recruiter working at top technology companies.

Your task is to generate a **structured role profile** for the given job title.

--------------------------------------------------

ROLE
{role}

--------------------------------------------------

Your job is to define what skills and technologies are required for this role.

Focus on **real industry expectations**.

--------------------------------------------------

STRUCTURE

core_skills  
Essential technical abilities required for this role.

supporting_skills  
Additional skills that improve candidate strength.

tools  
Frameworks, libraries, or developer tools used.

cloud  
Cloud platforms commonly used.

responsibilities  
Typical responsibilities for the role.

experience_level  
Entry Level / Mid Level / Senior.

--------------------------------------------------

RULES

• Do NOT guess unrealistic technologies.
• Use real industry standards.
• Avoid generic terms like "communication".
• Only include technical skills.

--------------------------------------------------

OUTPUT FORMAT

Return ONLY JSON.

{{
 "role_title": "{role}",
 "core_skills": [],
 "supporting_skills": [],
 "tools": [],
 "cloud": [],
 "responsibilities": [],
 "experience_level": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=700,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    print("RAW ROLE AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    data = json.loads(cleaned)

    return data