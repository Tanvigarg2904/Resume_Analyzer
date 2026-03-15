import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------------------------------
# JSON Cleaner
# ---------------------------------------------------------
def clean_json(raw):

    raw = raw.strip()

    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object detected")

    return raw[start:end+1]


# ---------------------------------------------------------
# Resume Improvement Agent
# ---------------------------------------------------------
def resume_agent(resume_text, role):

    prompt = f"""
You are a FAANG-level resume reviewer and technical hiring manager.

Your job is to rewrite weak resume bullet points into **high-impact recruiter-friendly achievements**.

------------------------------------------------

TARGET ROLE
{role}

------------------------------------------------

RESUME
{resume_text}

------------------------------------------------

TASK

Analyze the resume and identify bullet points that are:

• vague
• weak
• missing technologies
• missing measurable impact
• missing context

Rewrite them into **strong professional bullet points**.

------------------------------------------------

RULES

Every improved bullet point must include:

• strong action verbs
• technologies used
• measurable impact
• clear outcome

Use verbs like:

Designed
Developed
Engineered
Optimized
Implemented
Built
Automated
Scaled
Improved
Reduced
Accelerated

------------------------------------------------

GOOD EXAMPLE

Weak:

Worked on a machine learning model.

Improved:

Developed a machine learning classification model using Python and Scikit-learn that improved prediction accuracy by 18%.

------------------------------------------------

BAD EXAMPLE

Did some coding.

------------------------------------------------

OUTPUT FORMAT

Return ONLY JSON.

{{
 "resume_improvements":[
  {{
   "original_line":"",
   "improved_version":"",
   "reason":""
  }}
 ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=1200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    print("RAW RESUME AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    data = json.loads(cleaned)

    return data