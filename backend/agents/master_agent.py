import traceback

from backend.agents.role_agents import role_agent
from backend.agents.skill_extractor_agent import skill_extractor_agent
from backend.agents.ats_agent import ats_agent
from backend.agents.roadmap_agent import roadmap_agent
from backend.agents.project_agent import project_agent
from backend.agents.resume_agent import resume_agent
from backend.agents.job_agent import job_agent
from backend.agents.interview_agent import interview_agent

from backend.utils.skill_gap_engine import compute_skill_gap


def master_agent(resume_text: str, role: str):

    print("\n===== MASTER AGENT STARTED =====")

    result = {
        "target_role": role,
        "role_profile": {},
        "extracted_skills": {},
        "skill_gap": [],
        "ats_score": 0,
        "matched_skills": [],
        "missing_core_skills": [],
        "learning_roadmap": [],
        "recommended_projects": [],
        "recommended_jobs": [],
        "resume_improvements": [],
        "interview_questions": []
    }

    try:

        # ---------------- ROLE PROFILE ----------------
        try:
            print("Running Role Agent...")
            role_profile = role_agent(role)
            result["role_profile"] = role_profile
        except Exception as e:
            print("Role Agent Failed:", e)
            traceback.print_exc()
            role_profile = {}

        # ---------------- SKILL EXTRACTION ----------------
        try:
            print("Running Skill Extractor...")
            skills_data = skill_extractor_agent(resume_text)
            result["extracted_skills"] = skills_data
            user_skills = skills_data.get("all_skills", [])
        except Exception as e:
            print("Skill Extractor Failed:", e)
            traceback.print_exc()
            user_skills = []

        # ---------------- SKILL GAP ----------------
        try:
            print("Running Skill Gap Engine...")
            skill_gap = compute_skill_gap(role_profile, user_skills)
            result["matched_skills"] = skill_gap.get("matched_skills", [])
            result["missing_core_skills"] = skill_gap.get("missing_skills", [])
            result["skill_graph"] = skill_gap.get("skill_graph",[])
        except Exception as e:
            print("Skill Gap Engine Failed:", e)
            traceback.print_exc()

        # ---------------- ATS SCORING ----------------
        try:
            print("Running ATS Agent...")
            ats_result = agents.ats_agent.ats_agent(
                resume_text=resume_text,
                role_profile=role_profile,
                role=role
            )

            result["ats_score"] = ats_result.get("ats_score", 0)
            result["matched_skills"] = ats_result.get("matched_skills", [])
            result["missing_core_skills"] = ats_result.get("missing_core_skills", [])

        except Exception as e:
            print("ATS Agent Failed:", e)
            traceback.print_exc()

        matched_skills = result["matched_skills"]
        missing_skills = result["missing_core_skills"]

        # ---------------- ROADMAP ----------------
        try:
            print("Running Roadmap Agent...")
            roadmap = roadmap_agent(
                role=role,
                matched_skills=matched_skills,
                missing_skills=missing_skills
            )

            result["learning_roadmap"] = roadmap
        except Exception as e:
            print("Roadmap Agent Failed:", e)
            traceback.print_exc()

        # ---------------- PROJECTS ----------------
        try:
            print("Running Project Agent...")
            projects = project_agent(
                role=role,
                matched_skills=matched_skills,
                missing_skills=missing_skills
            )

            result["recommended_projects"] = projects.get("recommended_projects", [])
        except Exception as e:
            print("Project Agent Failed:", e)
            traceback.print_exc()

        # ---------------- RESUME IMPROVEMENTS ----------------
        try:
            print("Running Resume Agent...")
            resume_improvements = resume_agent(
                resume_text=resume_text,
                role=role
            )

            result["resume_improvements"] = resume_improvements.get("resume_improvements", [])
        except Exception as e:
            print("Resume Agent Failed:", e)
            traceback.print_exc()

        # ---------------- JOBS ----------------
        try:
            print("Running Job Agent...")
            jobs = job_agent(
                role=role,
                resume_text=resume_text
            )

            result["recommended_jobs"] = jobs
        except Exception as e:
            print("Job Agent Failed:", e)
            traceback.print_exc()

        # ---------------- INTERVIEW QUESTIONS ----------------
        try:
            print("Running Interview Agent...")
            interview_questions = interview_agent(
                role=role,
                skills=user_skills
            )

            result["interview_questions"] = interview_questions.get("interview_questions", [])
        except Exception as e:
            print("Interview Agent Failed:", e)
            traceback.print_exc()

        print("===== MASTER AGENT COMPLETED =====\n")

        return result

    except Exception as e:

        print("MASTER AGENT CRITICAL ERROR:", e)
        traceback.print_exc()

        return result