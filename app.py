from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from utils.parser import extract_text_from_file
from utils.extractor import extract_info
from utils.scorer import calculate_score
from utils.recommender import generate_recommendations

app = FastAPI()

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Running 🚀"}


# ---------------- MAIN API ----------------
@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        # ---------------- SAVE FILE ----------------
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------- PARSE RESUME ----------------
        resume_text = extract_text_from_file(temp_file_path)

        # ---------------- EXTRACT INFO ----------------
        extracted_data = extract_info(resume_text)

        # ---------------- PROCESS JOB DESCRIPTION ----------------
        job_skills = [skill.strip().lower() for skill in job_description.split(",")]

        # ---------------- CALCULATE SCORE ----------------
        score, matched_skills, missing_skills = calculate_score(
            extracted_data,
            job_skills
        )

        # ---------------- RECOMMENDATIONS ----------------
        recommendations = generate_recommendations(missing_skills)

        # ---------------- EXPLANATION (IMPROVED) ----------------
        explanation = f"""
Candidate matched {len(matched_skills)} out of {len(job_skills)} required skills.

Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}

Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

Experience Level: {extracted_data.get('Experience', 0)} years

Projects Done:
{chr(10).join(extracted_data.get('Projects', [])) if extracted_data.get('Projects') else 'No projects listed'}

Final Score: {score}%

This score is calculated based on skill matching, experience, and project relevance.
"""

        # ---------------- RESPONSE ----------------
        return {
            "extracted_data": extracted_data,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "explanation": explanation
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        # ---------------- CLEANUP ----------------
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)