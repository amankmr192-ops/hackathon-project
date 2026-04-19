def detect_domain(skills):
    skills_text = " ".join(skills).lower()

    if any(word in skills_text for word in ["python", "java", "ai", "ml", "data"]):
        return "tech"
    elif any(word in skills_text for word in ["marketing", "sales", "finance", "hr"]):
        return "management"
    elif any(word in skills_text for word in ["clinical", "surgery", "patient", "medical"]):
        return "medical"
    elif any(word in skills_text for word in ["civil", "mechanical", "electrical"]):
        return "engineering"
    else:
        return "general"


def generate_recommendations(missing_skills):
    recommendations = []
    domain = detect_domain(missing_skills)

    for skill in missing_skills:
        skill_lower = skill.lower()

        # Domain-based action
        if domain == "tech":
            action = f"Build projects and gain hands-on experience in {skill}"
        elif domain == "management":
            action = f"Improve {skill} through case studies, internships, and certifications"
        elif domain == "medical":
            action = f"Enhance {skill} via clinical exposure and practical training"
        elif domain == "engineering":
            action = f"Strengthen {skill} through real-world engineering projects"
        else:
            action = f"Learn {skill} through courses and practical exposure"

        # Universal resources
        resources = [
            f"YouTube search: '{skill} tutorial'",
            f"Take a course on Coursera/Udemy for {skill}",
            f"Build at least 1 project using {skill}"
        ]

        recommendations.append({
            "skill": skill,
            "recommendation": action,
            "resources": resources,
            "priority": "High"
        })

    return recommendations