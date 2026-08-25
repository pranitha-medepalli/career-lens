SKILL_RELATIONSHIPS = {

    "github": [
        "git"
    ],

    "git": [
        "github"
    ],

    "github actions": [
        "ci/cd"
    ],

    "ci/cd": [
        "github actions",
        "jenkins",
        "gitlab ci"
    ],

    "mysql": [
        "sql",
        "postgresql"
    ],

    "postgresql": [
        "sql",
        "mysql"
    ],

    "flask": [
        "rest api",
        "fastapi",
        "django"
    ],

    "fastapi": [
        "rest api",
        "flask",
        "django"
    ],

    "django": [
        "rest api",
        "flask",
        "fastapi"
    ]
}


def find_related_skill(
    job_skill: str,
    resume_skills: set
):

    job_skill = job_skill.lower()

    # Exact match
    if job_skill in resume_skills:

        return {
            "matched": True,
            "match_type": "EXACT",
            "resume_skill": job_skill
        }

    # Related skill match
    related_skills = (
        SKILL_RELATIONSHIPS
        .get(job_skill, [])
    )

    for related_skill in related_skills:

        if related_skill in resume_skills:

            return {
                "matched": True,
                "match_type": "RELATED",
                "resume_skill": related_skill
            }

    return {
        "matched": False,
        "match_type": None,
        "resume_skill": None
    }


def match_skills(
    resume_skills: set,
    job_skills: set
):

    exact_matches = []

    related_matches = []

    missing_skills = []

    for job_skill in job_skills:

        result = find_related_skill(
            job_skill,
            resume_skills
        )

        if result["matched"]:

            if (
                result["match_type"]
                == "EXACT"
            ):

                exact_matches.append(
                    job_skill
                )

            else:

                related_matches.append({
                    "job_skill": job_skill,
                    "related_resume_skill":
                        result["resume_skill"]
                })

        else:

            missing_skills.append(
                job_skill
            )

    return {
        "exact_matches":
            sorted(exact_matches),

        "related_matches":
            related_matches,

        "missing_skills":
            sorted(missing_skills)
    }