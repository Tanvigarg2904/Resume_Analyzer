from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.master_agent import master_agent
from agents.job_agent import job_agent, get_role_skills

from pypdf import PdfReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(file: UploadFile, role: str = Form(...)):

    reader = PdfReader(file.file)
    resume = ""

    for p in reader.pages:
        if p.extract_text():
            resume += p.extract_text()

    analysis = master_agent(resume, role)

    jobs = job_agent(role, resume)

    core_skills = get_role_skills(role)

    return {
    **analysis,
    "jobs": jobs,
    "core_role_skills": core_skills
}

