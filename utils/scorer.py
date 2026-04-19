from utils.semantic import semantic_match

def calculate_score(resume_skills, job_skills):
    """
    Calculates match score between resume skills and job skills
    using semantic similarity.
    """

    # Safety: handle empty inputs
    if not resume_skills:
        return 0, [], job_skills

    if not job_skills:
        return 0, [], []

    # Semantic matching
    matched_skills, missing_skills = semantic_match(
        resume_skills,
        job_skills
    )

    # Score calculation
    total_required = len(job_skills)
    matched_count = len(matched_skills)

    score = int((matched_count / total_required) * 100)

    return score, matched_skills, missing_skills