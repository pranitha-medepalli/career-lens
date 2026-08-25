def generate_suggestions(
    matched_skills,
    missing_skills,
    match_score
):

    suggestions = []

    if match_score < 50:

        suggestions.append({
            "priority": "HIGH",
            "type": "SKILL_GAP",
            "message": (
                "Your resume currently has a low "
                "match with this job description. "
                "Focus on developing the most important "
                "missing skills."
            )
        })

    for skill in missing_skills:

        suggestions.append({

            "priority": "MEDIUM",

            "type": "SKILL_TO_LEARN",

            "skill": skill,

            "message": (
                f"Consider gaining hands-on experience "
                f"with {skill}. Do not add it to your "
                f"resume until you have actually used it."
            )
        })

    if matched_skills:

        suggestions.append({

            "priority": "HIGH",

            "type": "HIGHLIGHT_SKILLS",

            "skills": matched_skills,

            "message": (
                "Make sure these matching skills are "
                "clearly visible in your Skills and "
                "Experience sections."
            )
        })

    return suggestions