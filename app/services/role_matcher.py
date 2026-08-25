from app.data.roles import ROLES


def suggest_roles(resume_skills):

    results = []

    resume_skills = set(
        skill.lower()
        for skill in resume_skills
    )

    for role, data in ROLES.items():

        required_skills = set(data["skills"])

        matched_skills = (
            resume_skills
            .intersection(required_skills)
        )

        missing_skills = (
            required_skills
            .difference(resume_skills)
        )

        if required_skills:

            score = (
                len(matched_skills)
                / len(required_skills)
                * 100
            )

        else:

            score = 0

        results.append({

            "role": role,

            "match_score": round(score, 2),

            "matching_skills": sorted(
                list(matched_skills)
            ),

            "missing_skills": sorted(
                list(missing_skills)
            )
        })

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results[:5]