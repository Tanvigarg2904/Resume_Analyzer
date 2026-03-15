import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------------------------------
# Utility: Clean JSON if model adds extra text
# ---------------------------------------------------------
def clean_json(raw: str) -> str:
    raw = raw.strip()

    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output")

    return raw[start:end + 1]


# ---------------------------------------------------------
# ATS Agent
# ---------------------------------------------------------
def ats_agent(resume_text: str, role_profile: dict, role: str):

    prompt = f"""
You are a senior technical recruiter with 15+ years of hiring experience at top technology companies such as Google, Amazon, Meta, Apple, and Microsoft.

Your task is to perform a realistic ATS-style resume evaluation.

--------------------------------------------------
TARGET ROLE
{role}

--------------------------------------------------
ROLE PROFILE
{json.dumps(role_profile, indent=2)}

--------------------------------------------------
CANDIDATE RESUME
{resume_text}

--------------------------------------------------

EVALUATION FRAMEWORK

Score the candidate using the following criteria.

Skill Match (40%)
Evaluate how well the candidate’s technical skills match the required core skills.

Project Depth (20%)
Evaluate project complexity, relevance to the role, and evidence of real implementation.

Experience Relevance (15%)
Evaluate internships, professional work, research work, or applied experience related to the role.

Keyword Optimization (10%)
Evaluate whether industry keywords appear in the resume.

Tool Alignment (10%)
Evaluate alignment between tools used in the resume and tools required in the role.

Impact (5%)
Evaluate measurable results such as performance improvements, metrics, optimization, revenue impact, etc.

--------------------------------------------------

SCORING RULES

All scores must be between 0 and 100.

90–100 → exceptional candidate  
75–89 → strong candidate  
60–74 → moderate readiness  
40–59 → weak alignment  
below 40 → poor alignment

--------------------------------------------------

TASK

1. Identify matched skills between resume and role profile
2. Identify missing core skills required for the role
3. Identify missing tools and technologies
4. Score the candidate using the evaluation framework

--------------------------------------------------

OUTPUT FORMAT

Return STRICT JSON only.

{{
 "skill_match": number,
 "project_depth": number,
 "experience_relevance": number,
 "keyword_optimization": number,
 "tool_alignment": number,
 "impact": number,
 "matched_skills": [],
 "missing_core_skills": [],
 "tool_gaps": []
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    print("RAW ATS AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    data = json.loads(cleaned)

    # ---------------------------------------------------------
    # Calculate ATS score using deterministic logic
    # ---------------------------------------------------------

    skill_match = data.get("skill_match", 0)
    project_depth = data.get("project_depth", 0)
    experience_relevance = data.get("experience_relevance", 0)
    keyword_optimization = data.get("keyword_optimization", 0)
    tool_alignment = data.get("tool_alignment", 0)
    impact = data.get("impact", 0)

    ats_score = int(
        skill_match * 0.4 +
        project_depth * 0.2 +
        experience_relevance * 0.15 +
        keyword_optimization * 0.1 +
        tool_alignment * 0.1 +
        impact * 0.05
    )

    data["ats_score"] = ats_score

    return data