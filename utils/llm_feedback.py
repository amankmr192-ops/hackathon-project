import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def generate_feedback(resume_data, job_description):
    """
    Generates HR-style feedback using Mistral API.
    Falls back to rule-based feedback if API key missing.
    """

    # -------- Fallback (NO API KEY) --------
    if not MISTRAL_API_KEY:
        return f"""
Candidate scored {resume_data['score']}%.

Strengths:
{', '.join(resume_data['matched_skills']) if resume_data['matched_skills'] else 'None'}

Weaknesses:
{', '.join(resume_data['missing_skills']) if resume_data['missing_skills'] else 'None'}

Suggestion:
Improve missing skills and build practical projects.
"""

    # -------- LLM CALL --------
    prompt = f"""
You are an expert HR recruiter.

Candidate:
Matched Skills: {resume_data['matched_skills']}
Missing Skills: {resume_data['missing_skills']}
Score: {resume_data['score']}%

Job Requirements:
{job_description}

Give:
1. Short evaluation
2. Strengths
3. Weaknesses
4. Suggestions
"""

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-small",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=20
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception:
        return "AI feedback unavailable. Showing basic analysis."