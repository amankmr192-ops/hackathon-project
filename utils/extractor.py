import re

def extract_info(text):
    text = text.lower()

    # Common skill keywords (multi-domain)
    skill_keywords = [
        # Tech
        "python", "java", "machine learning", "ai", "docker", "sql",
        "html", "css", "javascript", "react", "node",

        # Sales / Management
        "sales", "marketing", "lead generation", "crm", "negotiation",
        "communication", "client handling", "business development",

        # Finance
        "finance", "accounting", "banking", "financial analysis",

        # General
        "problem solving", "teamwork", "leadership"
    ]

    found_skills = []

    for skill in skill_keywords:
        if skill in text:
            found_skills.append(skill)

    return {
        "Skills": found_skills
    }