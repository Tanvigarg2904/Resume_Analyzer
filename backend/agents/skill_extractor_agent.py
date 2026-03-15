import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------------------------------
# JSON Cleaner (prevents parsing crashes)
# -----------------------------------------------------
def clean_json(raw):

    raw = raw.strip()

    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object detected")

    return raw[start:end+1]


# -----------------------------------------------------
# Skill Extractor Agent
# -----------------------------------------------------
def skill_extractor_agent(resume_text):

    prompt = f"""
You are an expert technical recruiter and resume parser.

Your job is to extract **technical skills only** from a resume.

--------------------------------------------------

RESUME
{resume_text}

--------------------------------------------------

TASK

Identify all technical skills in the resume and classify them into categories.

Avoid soft skills like:
communication
teamwork
leadership

Extract only **technical abilities**.

--------------------------------------------------

SKILL CATEGORIES

programming_languages
frameworks
databases
tools
cloud
machine_learning
concepts

--------------------------------------------------

EXAMPLES

Programming Languages
Python, Java, C++, JavaScript

Frameworks
React, Django, Flask, Spring Boot

Databases
MySQL, PostgreSQL, MongoDB

Tools
Git, Docker, Kubernetes

Cloud
AWS, GCP, Azure

Machine Learning
TensorFlow, PyTorch, Scikit-learn

Concepts
Data Structures
Algorithms
System Design
REST APIs
Microservices

--------------------------------------------------

RULES

Return ONLY valid JSON.

Do not include explanation text.

--------------------------------------------------

OUTPUT FORMAT

{{
 "skills": {{
  "programming_languages": [],
  "frameworks": [],
  "databases": [],
  "tools": [],
  "cloud": [],
  "machine_learning": [],
  "concepts": []
 }},
 "all_skills":[]
}}

"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    print("RAW SKILL EXTRACTOR AGENT OUTPUT:", raw)

    cleaned = clean_json(raw)

    data = json.loads(cleaned)

    return data