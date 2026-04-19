from fastapi import FastAPI, UploadFile, Form
from typing import List

from utils.parser import extract_text_from_file, extract_skills
from utils.scorer import calculate_score
from utils.recommender import get_recommendations
from utils.ranker import rank_resumes
from utils.llm_feedback import generate_feedback

app = FastAPI()


def detect_role(text):
    text = text.lower()

    if "sales" in text or "marketing" in text:
        return "Sales / Marketing"
    elif "machine learning" in text or "ai" in text:
        return "AI / ML Engineer"
    elif "finance" in text or "bank" in text:
        return "Finance / Banking"
    elif "doctor" in text or "medical" in text:
        return "Healthcare"
    return "General Profile"


@app.post("/analyze/")
async def analyze_resume(
    files: List[UploadFile],
    job_description: str = Form(...)
):
    results = []

    job_skills = [s.strip().lower() for s in job_description.split(",")]

    for file in files:
        text = extract_text_from_file(file)
        resume_skills = extract_skills(text)

        score, matched, missing = calculate_score(
            resume_skills,
            job_skills
        )

        recommendations = get_recommendations(missing)

        feedback = generate_feedback(
            {
                "matched_skills": matched,
                "missing_skills": missing,
                "score": score
            },
            job_description
        )

        role = detect_role(text)

        results.append({
            "name": file.filename,
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "recommendations": recommendations,
            "feedback": feedback,
            "predicted_role": role
        })

    ranked = rank_resumes(results)

    return {
        "ranked_results": ranked,
        "top_candidate": ranked[0] if ranked else None
    }