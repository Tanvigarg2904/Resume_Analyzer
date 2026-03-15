import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------------
# JSON Cleaner
# -------------------------------
def clean_json(raw):

    raw = raw.strip()

    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object detected")

    return raw[start:end+1]


# -------------------------------
# Interview Question Generator
# -------------------------------
def interview_agent(role, skills):

    prompt = f"""
You are a senior technical interviewer from top technology companies.

Your job is to generate **realistic technical interview questions**.

ROLE
{role}

CANDIDATE SKILLS
{skills}

-----------------------------------------

Generate **10 high-quality interview questions**.

Include multiple categories:

• Technical concepts  
• Coding questions  
• System design questions  
• Scenario questions  

Questions should match the role.

-----------------------------------------

Each question must include:

question  
difficulty (easy / medium / hard)  
expected_topics  
model_answer  
evaluation_criteria  

-----------------------------------------

Rules

• Questions must be realistic
• Avoid generic questions
• Match the candidate skill level
• Questions should reflect real interview patterns

-----------------------------------------

OUTPUT FORMAT

Return ONLY JSON.

{{
 "interview_questions":[
  {{
   "question":"",
   "difficulty":"",
   "expected_topics":[],
   "model_answer":"",
   "evaluation_criteria":[]
  }}
 ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    print("RAW INTERVIEW AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    try:
        data = json.loads(cleaned)
    except Exception as e:
        print("JSON Parsing Failed in Interview Agent:", e)
        print("CLEANED OUTPUT:", cleaned[:1000])
        data = {
            "interview_questions": []}

    return data