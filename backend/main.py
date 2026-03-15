import traceback
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pydantic import BaseModel
from typing import List,Optional,Dict

from agents.master_agent import master_agent
from agents.interview_chat_agent import interview_chat_agent
from agents.skill_extractor_agent import skill_extractor_agent


app = FastAPI()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "SkillForge AI Backend Running"}


# -----------------------------------
# RESUME ANALYSIS
# -----------------------------------

@app.post("/analyze")
async def analyze_resume(file: UploadFile, role: str = Form(...)):

    try:

        if not file.filename.endswith(".pdf"):
            return {
                "error": "Invalid file format. Please upload a PDF file."
            }

        # reset pointer
        file.file.seek(0)

        reader = PdfReader(file.file)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            print("Raw extracted text:", text)

            if text:
                resume_text += text + "\n"
                print("Extracted text from page")
            else:
                print("No text extracted from page")

        if len(resume_text.strip()) == 0:

            return {
                "error": "Resume text extraction failed"
            }

        result = master_agent(
            resume_text=resume_text,
            role=role
        )

        return result

    except Exception as e:

        print("ANALYZE ERROR")
        traceback.print_exc()

        return {
            "error": "Resume analysis failed"
        }


# -----------------------------------
# INTERVIEW CHAT
# -----------------------------------
class InterviewRequest(BaseModel):
    message: str
    role: Optional[str]
    resume_text:Optional[str] = ""
    chat_history: Optional[List[Dict]] = []
    

@app.post("/interview-chat")
async def interview_chat(data: InterviewRequest):

    try:

        # Extract skills from resume
        skills_data = skill_extractor_agent(data.resume_text)

        skills = skills_data.get("all_skills", [])

        response = interview_chat_agent(
            role=data.role,
            skills=[],
            resume_text=data.resume_text,
            chat_history=data.chat_history,
            message=data.message
        )

        return {"response": response}

    except Exception as e:
        print("INTERVIEW ERROR:", e)

        return {
            "response": "Something went wrong in the interview system."
        }