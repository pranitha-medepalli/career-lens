from app.services.skill_extractor import (
    extract_skills,
    get_flat_skills
)


def analyze_job_description(
    job_description: str
):

    categorized_skills = extract_skills(
        job_description
    )

    skills = get_flat_skills(
        categorized_skills
    )

    return {

        "categorized_skills":
            categorized_skills,

        "skills":
            skills
    }