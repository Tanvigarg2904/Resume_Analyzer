import os, json, re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM = """
You are SkillForge AI Pro.

You simulate:
- FAANG Recruiter
- ATS Scanner
- Hiring Manager
- Career Strategist

Return STRICT JSON ONLY.
No markdown.
No explanations.
No comments.
No ``` blocks.
"""

def force_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}") + 1

    return raw[start:end]


def master_agent(resume: str, role: str) -> dict:

    PROMPT = f"""
Target Role: {role}

Return JSON exactly in this schema:

{{
 "ats_score": number,
 "snapshot": {{
   "role_fit": "",
   "seniority": "",
   "readiness": ""
 }},
 "skills": {{
   "matched": [],
   "missing": []
 }},
 "gaps": [],
 "roadmap": {{
   "month1": [],
   "month2": [],
   "month3": []
 }},
 "projects": [
   {{"title": "", "description": ""}}
 ]
}}

Rules:
- ats_score realistic (30–80)
- gaps must block internships
- roadmap achievable in 90 days
- projects industry aligned
- JSON ONLY

Resume:
{resume}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT}
        ]
    )

    raw = response.choices[0].message.content
    cleaned = force_json(raw)

    try:
        return json.loads(cleaned)

    except Exception:
        print("\n⚠️ RAW MODEL OUTPUT (INVALID JSON):\n", raw)

        # ⛑️ FAILSAFE — NEVER CRASH API
        return {
            "ats_score": 0,
            "snapshot": {
                "role_fit": "Parsing Error",
                "seniority": "",
                "readiness": ""
            },
            "skills": {
                "matched": [],
                "missing": []
            },
            "gaps": ["LLM returned malformed JSON"],
            "roadmap": {
                "month1": [],
                "month2": [],
                "month3": []
            },
            "projects": []
        }
