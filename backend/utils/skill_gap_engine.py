def compute_skill_gap(role_profile, user_skills):

    core_skills = role_profile.get("core_technical_skills", [])
    supporting_skills = role_profile.get("supporting_technical_skills", [])
    tools = role_profile.get("tools_and_technologies", [])

    all_required_skills = core_skills + supporting_skills + tools

    skill_graph = []
    user_skill_set = {s.lower() for s in user_skills}

    for skill in all_required_skills:

        
        if skill.lower() in user_skill_set:

            status = "learned"
            score = 80

        else:

            status = "missing"
            score = 20

        skill_graph.append({
            "skill": skill,
            "user_level": score,
            "ideal_level": 90,
            "status": status
        })

    matched_skills = [s["skill"] for s in skill_graph if s["status"] == "learned"]
    missing_skills = [s["skill"] for s in skill_graph if s["status"] == "missing"]
    return{
        "matched_skills" : matched_skills,
        "missing_skills" : missing_skills,
        "skill_graph" : skill_graph
    }
    