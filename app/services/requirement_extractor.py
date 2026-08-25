import re

from app.services.skill_extractor import (
    extract_skills,
    get_flat_skills
)


ANY_OF_PATTERNS = [

    r"at least one of",

    r"one or more of",

    r"any of the following",

    r"one of the following",

    r"experience with either",

    r"proficiency in either",

    r"knowledge of either"
]


PREFERRED_KEYWORDS = [

    "preferred",

    "nice to have",

    "nice-to-have",

    "good to have",

    "bonus",

    "desired"
]


def is_any_of_requirement(text: str):

    text = text.lower()

    for pattern in ANY_OF_PATTERNS:

        if re.search(pattern, text):

            return True

    return False


def is_preferred_requirement(text: str):

    text = text.lower()

    for keyword in PREFERRED_KEYWORDS:

        if keyword in text:

            return True

    return False


def split_job_description(job_description: str):

    # Split by:
    # - line breaks
    # - bullet points
    # - sentence endings

    parts = re.split(

        r"\n+|•|\- |\.\s+(?=[A-Z])",

        job_description
    )

    cleaned_parts = []

    for part in parts:

        part = part.strip()

        if len(part) > 10:

            cleaned_parts.append(part)

    return cleaned_parts


def extract_requirements(job_description: str):

    sections = split_job_description(
        job_description
    )

    requirements = []

    for section in sections:

        skill_dict = extract_skills(
            section
        )

        skills = get_flat_skills(
            skill_dict
        )

        # --------------------------------
        # ANY_OF technical requirement
        # --------------------------------

        if (
            skills
            and is_any_of_requirement(section)
        ):

            requirements.append({

                "type": "ANY_OF",

                "priority": "REQUIRED",

                "source_text": section,

                "skills": skills
            })

            continue

        # --------------------------------
        # ALL_OF technical requirement
        # --------------------------------

        if skills:

            priority = "REQUIRED"

            if is_preferred_requirement(section):

                priority = "PREFERRED"

            requirements.append({

                "type": "ALL_OF",

                "priority": priority,

                "source_text": section,

                "skills": skills
            })

    return requirements