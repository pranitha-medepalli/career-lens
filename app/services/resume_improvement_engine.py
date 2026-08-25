from typing import Any


def get_priority_level(
    requirement: dict,
    status: str
) -> str:

    priority = requirement.get(
        "priority",
        "REQUIRED"
    )

    if status == "NO_EVIDENCE":

        if priority == "REQUIRED":
            return "HIGH"

        return "MEDIUM"

    if status == "PARTIAL_MATCH":

        if priority == "REQUIRED":
            return "HIGH"

        return "MEDIUM"

    if status == "NOT_VERIFIABLE":

        return "LOW"

    return "LOW"


def generate_skill_suggestion(
    requirement: dict,
    result: dict
):

    skills = requirement.get(
        "skills",
        []
    )

    matched_skills = result.get(
        "matched_skills",
        []
    )

    missing_skills = result.get(
        "missing_skills",
        []
    )

    requirement_type = requirement.get(
        "type",
        ""
    )

    status = result.get(
        "status",
        ""
    )

    # ------------------------------------
    # ANY_OF
    # ------------------------------------

    if requirement_type == "ANY_OF":

        if status == "STRONG_MATCH":

            return {
                "action": "HIGHLIGHT",
                "message": (
                    "Your resume already satisfies "
                    "this requirement. Make sure the "
                    "strongest matching technologies "
                    "are clearly visible in your "
                    "Technical Skills and Projects "
                    "sections."
                ),
                "matched_skills":
                    matched_skills
            }

        return {
            "action": "LEARN",
            "message": (
                "You do not currently demonstrate "
                "any of the accepted technologies. "
                "Gain hands-on experience with at "
                "least one of the technologies before "
                "adding it to your resume."
            ),
            "missing_skills":
                missing_skills
        }

    # ------------------------------------
    # ALL_OF
    # ------------------------------------

    if requirement_type == "ALL_OF":

        if status == "STRONG_MATCH":

            return {
                "action": "HIGHLIGHT",
                "message": (
                    "Your resume already demonstrates "
                    "this requirement. Make the "
                    "relevant experience more visible."
                ),
                "matched_skills":
                    matched_skills
            }

        if status == "PARTIAL_MATCH":

            return {
                "action": "REWRITE",
                "message": (
                    "You demonstrate part of this "
                    "requirement. Strengthen the "
                    "relevant project or experience "
                    "description instead of adding "
                    "unsupported skills."
                ),
                "matched_skills":
                    matched_skills,
                "missing_skills":
                    missing_skills
            }

        return {
            "action": "LEARN",
            "message": (
                "This requirement is not clearly "
                "demonstrated. Consider gaining "
                "hands-on experience before adding "
                "these skills to your resume."
            ),
            "missing_skills":
                missing_skills
        }

    return {
        "action": "REVIEW",
        "message":
            "Review this requirement manually."
    }


def generate_education_suggestion(
    result: dict
):

    status = result.get(
        "status",
        ""
    )

    if status == "STRONG_MATCH":

        return {
            "action": "HIGHLIGHT",
            "message": (
                "Your education already satisfies "
                "this requirement. Keep your degree "
                "and expected/completion date clearly "
                "visible."
            )
        }

    return {
        "action": "ADD_EVIDENCE",
        "message": (
            "Add your relevant degree, institution, "
            "field of study, and expected/completion "
            "date if applicable."
        )
    }


def generate_language_suggestion(
    result: dict
):

    status = result.get(
        "status",
        ""
    )

    if status == "NOT_VERIFIABLE":

        return {
            "action": "NOT_VERIFIABLE",
            "message": (
                "The resume does not provide enough "
                "evidence to verify this requirement. "
                "Do not treat the missing evidence as "
                "proof that you lack the ability."
            )
        }

    return {
        "action": "REVIEW",
        "message": (
            "Verify that your resume accurately "
            "represents the language ability requested "
            "by the employer."
        )
    }


def generate_writing_suggestion(
    result: dict
):

    status = result.get(
        "status",
        ""
    )

    if status == "STRONG_MATCH":

        return {
            "action": "HIGHLIGHT",
            "message": (
                "Your resume contains evidence relevant "
                "to written communication. Highlight "
                "technical documentation, written "
                "explanations, articles, or similar work "
                "if you have it."
            )
        }

    if status == "PARTIAL_MATCH":

        return {
            "action": "ADD_EVIDENCE",
            "message": (
                "Your resume shows some communication "
                "evidence, but not enough to establish "
                "strong writing ability. Consider adding "
                "genuine technical writing, documentation, "
                "blog posts, reports, or written explanations "
                "if applicable."
            )
        }

    return {
        "action": "NOT_VERIFIABLE",
        "message": (
            "The resume does not provide sufficient "
            "evidence to evaluate writing ability."
        )
    }


def generate_experience_suggestion(
    result: dict
):

    status = result.get(
        "status",
        ""
    )

    if status == "STRONG_MATCH":

        return {
            "action": "HIGHLIGHT",
            "message": (
                "Professional experience relevant "
                "to this requirement is already "
                "present. Emphasize the most relevant "
                "responsibilities and measurable impact."
            )
        }

    if status == "PARTIAL_MATCH":

        return {
            "action": "REWRITE",
            "message": (
                "Your projects demonstrate relevant "
                "software development ability, but "
                "the resume does not show conventional "
                "professional employment evidence. "
                "Strengthen project bullets with "
                "technologies, responsibilities, "
                "outcomes, and scale."
            )
        }

    return {
        "action": "LEARN",
        "message": (
            "No relevant software-development evidence "
            "was found. Consider gaining experience "
            "through internships, projects, open-source "
            "work, or professional roles."
        )
    }


def generate_generic_suggestion(
    result: dict
):

    status = result.get(
        "status",
        ""
    )

    if status == "STRONG_MATCH":

        return {
            "action": "HIGHLIGHT",
            "message": (
                "This requirement is already supported "
                "by evidence in your resume."
            )
        }

    if status == "PARTIAL_MATCH":

        return {
            "action": "REWRITE",
            "message": (
                "Your resume contains related evidence. "
                "Make the connection to the job requirement "
                "more explicit."
            )
        }

    return {
        "action": "REVIEW",
        "message": (
            "Review this requirement and determine "
            "whether you have genuine evidence that "
            "should be added to your resume."
        )
    }


def generate_requirement_suggestion(
    requirement: dict,
    result: dict
):

    requirement_type = requirement.get(
        "type",
        "UNKNOWN"
    )

    status = result.get(
        "status",
        ""
    )

    priority = get_priority_level(
        requirement,
        status
    )

    if requirement_type in (
        "ANY_OF",
        "ALL_OF"
    ):

        suggestion = generate_skill_suggestion(
            requirement,
            result
        )

    elif requirement_type == "EDUCATION":

        suggestion = generate_education_suggestion(
            result
        )

    elif requirement_type == "LANGUAGE":

        suggestion = generate_language_suggestion(
            result
        )

    elif requirement_type == "WRITING":

        suggestion = generate_writing_suggestion(
            result
        )

    elif requirement_type == "EXPERIENCE":

        suggestion = generate_experience_suggestion(
            result
        )

    else:

        suggestion = generate_generic_suggestion(
            result
        )

    return {

        "priority":
            priority,

        "requirement_type":
            requirement_type,

        "requirement":
            requirement.get(
                "source_text",
                ""
            ),

        "current_status":
            status,

        "action":
            suggestion.get(
                "action",
                "REVIEW"
            ),

        "message":
            suggestion.get(
                "message",
                ""
            ),

        "matched_skills":
            suggestion.get(
                "matched_skills",
                result.get(
                    "matched_skills",
                    []
                )
            ),

        "missing_skills":
            suggestion.get(
                "missing_skills",
                result.get(
                    "missing_skills",
                    []
                )
            ),

        "evidence":
            result.get(
                "evidence",
                []
            )
    }


def generate_resume_improvements(
    requirements: list,
    requirement_results: list
):

    improvements = []

    for requirement, result in zip(
        requirements,
        requirement_results
    ):

        improvement = (
            generate_requirement_suggestion(
                requirement,
                result
            )
        )

        improvements.append(
            improvement
        )

    # Sort highest priority first.

    priority_order = {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 2
    }

    improvements.sort(
        key=lambda item:
            priority_order.get(
                item["priority"],
                3
            )
    )

    summary = {

        "high_priority":
            sum(
                1
                for item in improvements
                if item["priority"] == "HIGH"
            ),

        "medium_priority":
            sum(
                1
                for item in improvements
                if item["priority"] == "MEDIUM"
            ),

        "low_priority":
            sum(
                1
                for item in improvements
                if item["priority"] == "LOW"
            )
    }

    return {

        "summary":
            summary,

        "improvements":
            improvements
    }