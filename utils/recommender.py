def get_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:
        recommendations.append({
            "skill": skill,
            "advice": f"Improve your {skill} with practical experience and learning.",
            "resources": [
                f"Search on YouTube: '{skill} tutorial'",
                f"Take courses on Coursera/Udemy for {skill}",
                f"Read official docs of {skill}"
            ],
            "projects": [
                f"Build 1 project using {skill}",
                f"Apply {skill} in real-world scenarios"
            ]
        })

    return recommendations