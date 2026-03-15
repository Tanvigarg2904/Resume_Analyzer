import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------------------------------
# Clean JSON helper
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
# Project Recommendation Agent
# ---------------------------------------------------------
def project_agent(role, matched_skills, missing_skills):

    prompt = f"""
You are a senior software engineer and technical hiring manager at companies like Google, Amazon, and Microsoft.

Your job is to recommend **high-quality portfolio projects** that help a candidate become competitive for the target role.

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

Generate **3 portfolio-level projects**.

These projects must:

• strengthen the candidate's missing skills  
• demonstrate real-world engineering ability  
• be impressive to recruiters  

Avoid beginner projects like:

- Iris classification
- Titanic prediction
- Todo list apps

Instead suggest **realistic industry projects**.

------------------------------------------------

PROJECT REQUIREMENTS

Each project must include:

• project_name  
• problem_statement  
• tech_stack  
• system_design_overview  
• major_features  
• dataset_or_api  
• learning_outcomes  
• why_this_impresses_recruiters  
• estimated_ats_boost  

------------------------------------------------

EXAMPLES OF GOOD PROJECT TYPES

Machine Learning
- Fraud detection system
- Recommendation engine
- Real-time sentiment analysis

Backend
- Scalable microservice API
- Distributed job scheduler
- Event-driven architecture system

AI/LLM
- Document search engine
- AI coding assistant
- Chatbot with retrieval augmentation

------------------------------------------------

OUTPUT FORMAT

Return ONLY JSON.

{{
 "recommended_projects":[
   {{
     "project_name":"",
     "problem_statement":"",
     "tech_stack":[],
     "system_design_overview":"",
     "major_features":[],
     "dataset_or_api":"",
     "learning_outcomes":[],
     "why_this_impresses_recruiters":"",
     "estimated_ats_boost":""
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
    print("RAW PROJECT AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    data = json.loads(cleaned)

    return data