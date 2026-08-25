from app.services.skill_matcher import (
    find_related_skill
)


def match_requirement(
    requirement,
    resume_skills,
    resume_analysis
):

    requirement_type = requirement["type"]

    priority = requirement["priority"]

    # =================================
    # EDUCATION MATCHING
    # =================================

    if requirement_type == "EDUCATION":

        education = resume_analysis["education"]

        satisfied = education[
            "has_bachelor_degree"
        ]

        return {

            "type": "EDUCATION",

            "priority": priority,

            "source_text":
                requirement["source_text"],

            "requirement_satisfied":
                satisfied,

            "score":
                100 if satisfied else 0
        }

    # =================================
    # EXPERIENCE MATCHING
    # =================================

    if requirement_type == "EXPERIENCE":

        experience = resume_analysis["experience"]

        satisfied = experience[
            "has_relevant_experience"
        ]

        return {

            "type": "EXPERIENCE",

            "priority": priority,

            "source_text":
                requirement["source_text"],

            "requirement_satisfied":
                satisfied,

            "score":
                100 if satisfied else 0
        }

    # =================================
    # LANGUAGE MATCHING
    # =================================

    if requirement_type == "LANGUAGE":

        language = resume_analysis["language"]

        satisfied = language[
            "english_detected"
        ]

        return {

            "type": "LANGUAGE",

            "priority": priority,

            "source_text":
                requirement["source_text"],

            "requirement_satisfied":
                satisfied,

            "score":
                100 if satisfied else 0
        }

    # =================================
    # WRITING MATCHING
    # =================================

    if requirement_type == "WRITING":

        writing = resume_analysis["writing"]

        satisfied = writing[
            "writing_evidence_found"
        ]

        return {

            "type": "WRITING",

            "priority": priority,

            "source_text":
                requirement["source_text"],

            "requirement_satisfied":
                satisfied,

            "score":
                100 if satisfied else 0
        }

    # =================================
    # TECHNICAL SKILL MATCHING
    # =================================

    required_skills = requirement["skills"]

    matched_skills = []

    related_matches = []

    missing_skills = []

    for skill in required_skills:

        result = find_related_skill(
            skill,
            resume_skills
        )

        if result["matched"]:

            if result["match_type"] == "EXACT":

                matched_skills.append(
                    skill
                )

            else:

                related_matches.append({

                    "job_skill":
                        skill,

                    "related_resume_skill":
                        result["resume_skill"]
                })

        else:

            missing_skills.append(
                skill
            )

    # =================================
    # ANY_OF REQUIREMENT
    # =================================

    if requirement_type == "ANY_OF":

        satisfied = (

            len(matched_skills) > 0

            or

            len(related_matches) > 0
        )

        score = 100 if satisfied else 0

    # =================================
    # ALL_OF REQUIREMENT
    # =================================

    else:

        total_skills = len(
            required_skills
        )

        if total_skills == 0:

            score = 0

        else:

            score = round(

                (
                    len(matched_skills)
                    +
                    len(related_matches) * 0.5
                )

                /

                total_skills

                * 100,

                2
            )

        satisfied = score >= 70

    return {

        "type": requirement_type,

        "priority": priority,

        "source_text":
            requirement["source_text"],

        "skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "related_matches":
            related_matches,

        "missing_skills":
            missing_skills,

        "requirement_satisfied":
            satisfied,

        "score":
            score
    }


# =====================================
# MATCH ALL REQUIREMENTS
# =====================================

def match_all_requirements(
    requirements,
    resume_skills,
    resume_analysis
):

    results = []

    for requirement in requirements:

        result = match_requirement(

            requirement,
            resume_skills,
            resume_analysis
        )

        results.append(
            result
        )

    return results