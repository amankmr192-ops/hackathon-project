def calculate_score(extracted_data, job_skills):
    resume_skills = [skill.lower() for skill in extracted_data.get("Skills", [])]

    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Score calculation
    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matched_skills) / len(job_skills)) * 100)

    return score, matched_skills, missing_skills