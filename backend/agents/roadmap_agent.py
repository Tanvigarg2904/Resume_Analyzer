import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------------------------------
# JSON Cleaner (prevents parsing crashes)
# ---------------------------------------------------------
def clean_json(raw: str):

    raw = raw.strip()

    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object detected in model output")

    return raw[start:end+1]


# ---------------------------------------------------------
# Roadmap Agent
# ---------------------------------------------------------
def roadmap_agent(role, matched_skills, missing_skills):

    prompt = f"""
You are a world-class AI career mentor and senior engineer who has mentored students that later joined companies like Google, Microsoft, Amazon, and Meta.

Your task is to generate a **highly practical and personalized 3-month learning roadmap**.

------------------------------------------------

TARGET ROLE
{role}

------------------------------------------------

CANDIDATE CURRENT SKILLS
{matched_skills}

------------------------------------------------

CANDIDATE MISSING SKILLS
{missing_skills}

------------------------------------------------

GOAL

Create a roadmap that helps the candidate move from their current skill level to the target role.

Avoid recommending topics the candidate already knows.

Focus on **missing skills and advanced improvements**.

------------------------------------------------

ROADMAP STRUCTURE

Month 1 → Foundations  
Month 2 → Advanced Skill Development  
Month 3 → Projects + Interview Preparation  

Each month must contain **4 weeks**.

Each week must include:

• focus topic  
• key learning goals  
• recommended resources  
• coding practice  
• mini project idea  

------------------------------------------------

Return ONLY valid JSON.

Do NOT include explanations.  
Do NOT include markdown.  
Do NOT include ```json.

------------------------------------------------

OUTPUT FORMAT

{{
 "learning_roadmap":[
   {{
     "month":"",
     "weeks":[
       {{
         "week":"",
         "focus":"",
         "goals":[],
         "resources":[],
         "practice":[],
         "mini_project":""
       }}
     ]
   }}
 ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=2500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    print("RAW ROADMAP AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    try:
        data = json.loads(cleaned)
    except Exception as e:
        print("JSON Parsing Failed in Roadmap Agent:", e)
        print("CLEANED OUTPUT:", cleaned[:1000])  # Print the first 1000 characters of cleaned output for debugging
        data = {
            "learning_roadmap": []}

    return data.get("learning_roadmap", [])
