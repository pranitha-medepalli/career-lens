import re


def analyze_education(resume_text: str):

    text = resume_text.lower()

    bachelor_keywords = [

        "b.tech",

        "btech",

        "bachelor of technology",

        "bachelor of engineering",

        "b.e.",

        "bachelor of science",

        "b.sc"
    ]

    for keyword in bachelor_keywords:

        if keyword in text:

            return {

                "has_bachelor_degree": True,

                "status": "IN_PROGRESS_OR_COMPLETED"
            }

    return {

        "has_bachelor_degree": False,

        "status": "NOT_FOUND"
    }


def analyze_experience(resume_text: str):

    text = resume_text.lower()

    experience_keywords = [

        "experience",

        "internship",

        "software developer",

        "software engineer",

        "developer",

        "programmer",

        "intern"
    ]

    for keyword in experience_keywords:

        if keyword in text:

            return {

                "has_relevant_experience": True
            }

    return {

        "has_relevant_experience": False
    }


def analyze_language(resume_text: str):

    text = resume_text.lower()

    english_keywords = [

        "english",

        "communication",

        "fluent"
    ]

    for keyword in english_keywords:

        if keyword in text:

            return {

                "english_detected": True
            }

    return {

        "english_detected": False
    }


def analyze_writing(resume_text: str):

    text = resume_text.lower()

    writing_keywords = [

        "documentation",

        "technical writing",

        "writing",

        "content"
    ]

    for keyword in writing_keywords:

        if keyword in text:

            return {

                "writing_evidence_found": True
            }

    return {

        "writing_evidence_found": False
    }


def analyze_resume_requirements(
    resume_text: str
):

    return {

        "education":
            analyze_education(
                resume_text
            ),

        "experience":
            analyze_experience(
                resume_text
            ),

        "language":
            analyze_language(
                resume_text
            ),

        "writing":
            analyze_writing(
                resume_text
            )
    }