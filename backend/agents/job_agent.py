import requests
from dotenv import load_dotenv
from groq import Groq
import os, re, json

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")
llm = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 1️⃣ Get dynamic core skills based on role
def get_role_skills(role: str):

    prompt = f"""
You are a technical recruiter.

Given the job role: "{role}",
list 8–12 core technical skills required for this role.

Return ONLY a JSON array of strings.
No explanation. No markdown.

Example:
["skill1","skill2","skill3"]
"""

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    raw = re.sub(r"```.*?\n", "", raw)
    raw = re.sub(r"```", "", raw)

    try:
        return json.loads(raw)
    except:
        # Safe fallback
        return role.lower().split()


# 2️⃣ Score each job using ATS logic
def score_job(job_text: str, resume_text: str, role: str):

    core_skills = get_role_skills(role)

    resume = resume_text.lower()
    job = job_text.lower()

    matched = []
    missing = []

    for skill in core_skills:
        s = skill.lower()
        if s in job and s in resume:
            matched.append(skill)
        elif s in job:
            missing.append(skill)

    # ATS scoring logic (simple but effective)
    score = min(95, max(25, len(matched) * 12))

    return score, matched, missing


# 3️⃣ Job agent with ATS-ranked results
def job_agent(role: str, resume_text: str, location="India"):

    if not SERP_API_KEY:
        return []

    params = {
        "engine": "google_jobs",
        "q": f"{role} internship",
        "location": location,
        "api_key": SERP_API_KEY
    }

    res = requests.get("https://serpapi.com/search.json", params=params)
    data = res.json()

    ranked_jobs = []

    for j in data.get("jobs_results", [])[:10]:

        apply_link = ""
        if j.get("apply_options"):
            apply_link = j["apply_options"][0].get("link", "")

        description = j.get("description", "")

        score, matched, missing = score_job(description, resume_text, role)

        ranked_jobs.append({
            "title": j.get("title", ""),
            "company": j.get("company_name", ""),
            "location": j.get("location", ""),
            "link": apply_link,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    # 4️⃣ Sort by ATS match
    ranked_jobs.sort(key=lambda x: x["match_score"], reverse=True)

    return ranked_jobs
