from app.services.skill_matcher import (
    find_related_skill
)


def normalize(value: str):

    if not value:
        return ""

    return value.lower().strip()


def get_resume_technical_skills(
    resume_evidence: dict
):

    skills = set()

    projects = (
        resume_evidence
        .get("projects", {})
        .get("items", [])
    )

    for project in projects:

        for technology in project.get(
            "technologies",
            []
        ):

            skills.add(
                normalize(technology)
            )

    return skills


def match_any_of_requirement(
    requirement: dict,
    resume_evidence: dict
):

    job_skills = requirement.get(
        "skills",
        []
    )

    resume_skills = set()

    # --------------------------------
    # Skills from project technologies
    # --------------------------------

    projects = (
        resume_evidence
        .get("projects", {})
        .get("items", [])
    )

    for project in projects:

        for technology in project.get(
            "technologies",
            []
        ):

            resume_skills.add(
                normalize(technology)
            )

    # --------------------------------
    # Skills from the resume's
    # technical-skills section
    # --------------------------------

    skills_text = (
        resume_evidence
        .get("sections", {})
        .get("skills", "")
    )

    # Import the same skill extraction
    # logic used by the main analyzer.

    from app.services.skill_extractor import (
        extract_skills,
        get_flat_skills
    )

    extracted = extract_skills(
        skills_text
    )

    for skill in get_flat_skills(
        extracted
    ):

        resume_skills.add(
            normalize(skill)
        )

    matched = []

    missing = []

    for skill in job_skills:

        normalized_skill = normalize(
            skill
        )

        # Exact match
        if normalized_skill in resume_skills:

            matched.append(skill)

            continue

        # Related skill
        result = find_related_skill(
            normalized_skill,
            resume_skills
        )

        if result["matched"]:

            matched.append(skill)

        else:

            missing.append(skill)

    satisfied = len(matched) > 0

    return {

        "status":
            "STRONG_MATCH"
            if satisfied
            else "NO_EVIDENCE",

        "confidence":
            100
            if satisfied
            else 0,

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "evidence": []
    }

def match_education_requirement(
    resume_evidence: dict
):

    education = resume_evidence.get(
        "education",
        {}
    )

    degree_evidence = education.get(
        "degree_evidence",
        []
    )

    if degree_evidence:

        return {

            "status":
                "STRONG_MATCH",

            "confidence":
                100,

            "evidence": [

                {
                    "source":
                        "education",

                    "text":
                        evidence
                }

                for evidence
                in degree_evidence
            ]
        }

    return {

        "status":
            "NO_EVIDENCE",

        "confidence":
            0,

        "evidence": []
    }


def match_language_requirement(
    resume_evidence: dict
):

    # Do not assume English ability simply
    # because a resume is written in English.
    #
    # Unless explicit evidence exists,
    # return NOT_VERIFIABLE rather than
    # incorrectly marking it as missing.

    return {

        "status":
            "NOT_VERIFIABLE",

        "confidence":
            0,

        "evidence": []
    }


def match_writing_requirement(
    resume_evidence: dict
):

    evidence = []

    # Mentorship can provide meaningful
    # communication/writing evidence.
    mentorship = (
        resume_evidence
        .get("mentorship", {})
        .get("items", [])
    )

    if mentorship:

        evidence.append({

            "source":
                "mentorship",

            "text":
                mentorship[0]
        })

    # Presentations/awards can also provide
    # some communication evidence.
    achievements = (
        resume_evidence
        .get("achievements", {})
        .get("items", [])
    )

    for achievement in achievements:

        if (
            "presented"
            in achievement.lower()
        ):

            evidence.append({

                "source":
                    "achievement",

                "text":
                    achievement
            })

    if evidence:

        return {

            "status":
                "PARTIAL_MATCH",

            "confidence":
                60,

            "evidence":
                evidence[:3]
        }

    return {

        "status":
            "NOT_VERIFIABLE",

        "confidence":
            0,

        "evidence": []
    }


def match_experience_requirement(
    resume_evidence: dict
):

    evidence = []

    # ------------------------------------
    # Actual professional experience
    # ------------------------------------

    experience = (
        resume_evidence
        .get("experience", {})
        .get("items", [])
    )

    if experience:

        evidence.extend([

            {
                "source":
                    "experience",

                "text":
                    item
            }

            for item in experience
        ])

    # ------------------------------------
    # Projects provide evidence of
    # software development, but they
    # are not equivalent to employment.
    # ------------------------------------

    projects = (
        resume_evidence
        .get("projects", {})
        .get("items", [])
    )

    for project in projects:

        title = project.get(
            "title",
            ""
        )

        if title:

            evidence.append({

                "source":
                    "project",

                "text":
                    title
            })

    # ------------------------------------
    # Mentorship demonstrates coding
    # experience and technical ability.
    # ------------------------------------

    mentorship = (
        resume_evidence
        .get("mentorship", {})
        .get("items", [])
    )

    if mentorship:

        evidence.append({

            "source":
                "mentorship",

            "text":
                mentorship[1]
                if len(mentorship) > 1
                else mentorship[0]
        })

    # ------------------------------------
    # Determine result
    # ------------------------------------

    if experience:

        return {

            "status":
                "STRONG_MATCH",

            "confidence":
                100,

            "evidence":
                evidence[:5]
        }

    if projects:

        return {

            "status":
                "PARTIAL_MATCH",

            "confidence":
                70,

            "evidence":
                evidence[:5]
        }

    return {

        "status":
            "NO_EVIDENCE",

        "confidence":
            0,

        "evidence": []
    }


def generate_recommendation(
    requirement_type,
    status
):

    if requirement_type == "LANGUAGE":

        if status == "NOT_VERIFIABLE":

            return (
                "The resume does not provide "
                "enough explicit evidence to verify "
                "English fluency. This should not "
                "be treated as a failure."
            )

    if requirement_type == "EDUCATION":

        if status == "STRONG_MATCH":

            return (
                "Your bachelor's degree requirement "
                "is directly supported by your "
                "education section."
            )

        return (
            "Add your bachelor's degree clearly "
            "with its expected/completion date."
        )

    if requirement_type == "WRITING":

        if status == "PARTIAL_MATCH":

            return (
                "Your mentorship and presentation "
                "activities provide some evidence of "
                "communication ability. Consider "
                "highlighting technical writing, "
                "documentation, or written explanations "
                "if you have them."
            )

        return (
            "No strong writing evidence was found. "
            "Consider highlighting documentation, "
            "technical articles, or written explanations "
            "if you have genuine experience."
        )

    if requirement_type == "EXPERIENCE":

        if status == "PARTIAL_MATCH":

            return (
                "Your projects demonstrate software "
                "development experience, but they are "
                "not equivalent to professional employment. "
                "Present them prominently and consider "
                "adding internships or developer experience "
                "when applicable."
            )

        return (
            "No professional software-development "
            "experience was found."
        )

    if requirement_type in (
        "ANY_OF",
        "ALL_OF"
    ):

        if status == "STRONG_MATCH":

            return (
                "The resume directly demonstrates "
                "the required technical skills."
            )

        return (
            "Do not add missing skills unless you "
            "have genuine hands-on experience."
        )

    return (
        "Review this requirement and provide "
        "supporting evidence if available."
    )


def match_requirement_with_evidence(
    requirement,
    resume_evidence
):

    requirement_type = requirement.get(
        "type"
    )

    priority = requirement.get(
        "priority",
        "REQUIRED"
    )

    # ====================================
    # ANY OF / ALL OF
    # ====================================

    if requirement_type == "ANY_OF":

        result = match_any_of_requirement(
            requirement,
            resume_evidence
        )

        return {

            "requirement":
                requirement.get(
                    "source_text",
                    ""
                ),

            "type":
                requirement_type,

            "priority":
                priority,

            "skills":
                requirement.get(
                    "skills",
                    []
                ),

            "status":
                result["status"],

            "confidence":
                result["confidence"],

            "matched_skills":
                result["matched_skills"],

            "missing_skills":
                result["missing_skills"],

            "evidence":
                result["evidence"],

            "recommendation":
                generate_recommendation(
                    requirement_type,
                    result["status"]
                )
        }

    # ====================================
    # EDUCATION
    # ====================================

    if requirement_type == "EDUCATION":

        result = match_education_requirement(
            resume_evidence
        )

        return {

            "requirement":
                requirement.get(
                    "source_text",
                    ""
                ),

            "type":
                requirement_type,

            "priority":
                priority,

            "skills": [],

            "status":
                result["status"],

            "confidence":
                result["confidence"],

            "matched_skills": [],

            "missing_skills": [],

            "evidence":
                result["evidence"],

            "recommendation":
                generate_recommendation(
                    requirement_type,
                    result["status"]
                )
        }

    # ====================================
    # LANGUAGE
    # ====================================

    if requirement_type == "LANGUAGE":

        result = match_language_requirement(
            resume_evidence
        )

        return {

            "requirement":
                requirement.get(
                    "source_text",
                    ""
                ),

            "type":
                requirement_type,

            "priority":
                priority,

            "skills": [],

            "status":
                result["status"],

            "confidence":
                result["confidence"],

            "matched_skills": [],

            "missing_skills": [],

            "evidence":
                result["evidence"],

            "recommendation":
                generate_recommendation(
                    requirement_type,
                    result["status"]
                )
        }

    # ====================================
    # WRITING
    # ====================================

    if requirement_type == "WRITING":

        result = match_writing_requirement(
            resume_evidence
        )

        return {

            "requirement":
                requirement.get(
                    "source_text",
                    ""
                ),

            "type":
                requirement_type,

            "priority":
                priority,

            "skills": [],

            "status":
                result["status"],

            "confidence":
                result["confidence"],

            "matched_skills": [],

            "missing_skills": [],

            "evidence":
                result["evidence"],

            "recommendation":
                generate_recommendation(
                    requirement_type,
                    result["status"]
                )
        }

    # ====================================
    # EXPERIENCE
    # ====================================

    if requirement_type == "EXPERIENCE":

        result = match_experience_requirement(
            resume_evidence
        )

        return {

            "requirement":
                requirement.get(
                    "source_text",
                    ""
                ),

            "type":
                requirement_type,

            "priority":
                priority,

            "skills": [],

            "status":
                result["status"],

            "confidence":
                result["confidence"],

            "matched_skills": [],

            "missing_skills": [],

            "evidence":
                result["evidence"],

            "recommendation":
                generate_recommendation(
                    requirement_type,
                    result["status"]
                )
        }

    # ====================================
    # Fallback
    # ====================================

    return {

        "requirement":
            requirement.get(
                "source_text",
                ""
            ),

        "type":
            requirement_type,

        "priority":
            priority,

        "skills":
            requirement.get(
                "skills",
                []
            ),

        "status":
            "NOT_VERIFIABLE",

        "confidence":
            0,

        "matched_skills": [],

        "missing_skills": [],

        "evidence": [],

        "recommendation":
            "The system could not reliably "
            "evaluate this requirement."
    }


def match_requirements_with_resume(
    requirements,
    resume_evidence
):

    results = []

    for requirement in requirements:

        result = match_requirement_with_evidence(
            requirement,
            resume_evidence
        )

        results.append(
            result
        )

    strong_matches = sum(
        1
        for result in results
        if result["status"]
        == "STRONG_MATCH"
    )

    partial_matches = sum(
        1
        for result in results
        if result["status"]
        == "PARTIAL_MATCH"
    )

    no_evidence = sum(
        1
        for result in results
        if result["status"]
        == "NO_EVIDENCE"
    )

    not_verifiable = sum(
        1
        for result in results
        if result["status"]
        == "NOT_VERIFIABLE"
    )

    return {

        "summary": {

            "total_requirements":
                len(results),

            "strong_matches":
                strong_matches,

            "partial_matches":
                partial_matches,

            "no_evidence":
                no_evidence,

            "not_verifiable":
                not_verifiable
        },

        "requirements":
            results
    }