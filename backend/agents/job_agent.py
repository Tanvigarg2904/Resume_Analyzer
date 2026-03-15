import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")


# ---------------------------------------------------------
# Detect job type
# ---------------------------------------------------------
def detect_job_type(job):

    title = job.get("title", "").lower()
    desc = job.get("description", "").lower()
    location = job.get("location", "").lower()

    if "intern" in title or "internship" in desc:
        return "Internship"

    if "remote" in title or "remote" in desc:
        return "Remote"

    if "work from home" in desc or "wfh" in desc:
        return "Work From Home"

    return "Full Time"


# ---------------------------------------------------------
# Job Agent
# ---------------------------------------------------------
def job_agent(role, resume_text, location="India"):

    if not SERP_API_KEY:
        print("SERPAPI_KEY missing")
        return {
            "internships": [],
            "remote": [],
            "work_from_home": [],
            "full_time": []
        }

    params = {
        "engine": "google_jobs",
        "q": f"{role} internship fresher",
        "location": location,
        "api_key": SERP_API_KEY
    }

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params
    )

    data = response.json()

    print("SERP Jobs Found:", len(data.get("jobs_results", [])))

    jobs = []

    for job in data.get("jobs_results", [])[:20]:

        title = job.get("title", "")
        company = job.get("company_name", "")
        location = job.get("location", "")
        description = job.get("description", "")

        # -------------------------------------------------
        # Extract apply link
        # -------------------------------------------------
        apply_link = ""

        apply_options = job.get("apply_options", [])

        if apply_options:
            apply_link = apply_options[0].get("link", "")

        if not apply_link:
            related = job.get("related_links", [])
            if related:
                apply_link = related[0].get("link", "")

        # fallback link
        if not apply_link:
            apply_link = "https://www.google.com/search?q=" + title.replace(" ", "+")

        salary = job.get(
            "detected_extensions",
            {}
        ).get("salary", "Not specified")

        job_type = detect_job_type(job)

        jobs.append({
            "job_title": title,
            "company": company,
            "location": location,
            "job_type": job_type,
            "salary_range": salary,
            "apply_link": apply_link,
            "description": description[:200],
            "match_percentage": 70,
            "reason": "Matches your selected role",
            "missing_requirements": []
        })

    # ---------------------------------------------------------
    # Group jobs by category
    # ---------------------------------------------------------
    grouped_jobs = {
        "internships": [],
        "remote": [],
        "work_from_home": [],
        "full_time": []
    }

    for job in jobs:

        if job["job_type"] == "Internship":
            grouped_jobs["internships"].append(job)

        elif job["job_type"] == "Remote":
            grouped_jobs["remote"].append(job)

        elif job["job_type"] == "Work From Home":
            grouped_jobs["work_from_home"].append(job)

        else:
            grouped_jobs["full_time"].append(job)

    print("Internships:", len(grouped_jobs["internships"]))
    print("Remote:", len(grouped_jobs["remote"]))
    print("Work From Home:", len(grouped_jobs["work_from_home"]))
    print("Full Time:", len(grouped_jobs["full_time"]))

    return grouped_jobs