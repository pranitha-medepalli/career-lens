import re

from app.services.skill_extractor import (
    extract_skills,
    get_flat_skills
)


REQUIREMENT_HEADERS = [
    "qualifications",
    "requirements",
    "required qualifications",
    "required skills",
    "what you'll need",
    "what you will need",
    "minimum qualifications",
    "technical requirements",
    "who you are",
    "skills and qualifications"
]


STOP_HEADERS = [
    "note",
    "notes",
    "responsibilities",
    "advantages",
    "benefits",
    "about the company",
    "about us",
    "compensation",
    "salary",
    "pay",
    "what we offer",
    "equal opportunity",
    "how to apply",
    "application process"
]


PREFERRED_PHRASES = [
    "preferred",
    "nice to have",
    "nice-to-have",
    "good to have",
    "bonus",
    "desired",
    "a plus",
    "plus"
]


ANY_OF_PATTERNS = [
    r"at least one of",
    r"one or more of",
    r"one of the following",
    r"any of the following",
    r"either .* or"
]


def normalize_for_search(text: str):

    text = text.lower()

    text = text.replace(
        "\u2019",
        "'"
    )

    text = text.replace(
        "\u2018",
        "'"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def find_header_position(
    text: str,
    headers: list[str]
):

    normalized_text = normalize_for_search(
        text
    )

    for header in headers:

        normalized_header = (
            normalize_for_search(header)
        )

        # Accept:
        # Qualifications
        # Qualifications:
        # Qualifications -
        # Qualifications \n
        pattern = re.compile(
            rf"\b{re.escape(normalized_header)}\b"
            rf"\s*(?::|-)?"
        )

        match = pattern.search(
            normalized_text
        )

        if match:

            return match

    return None


def extract_requirement_section(
    job_description: str
):

    text = job_description.strip()

    start_match = find_header_position(
        text,
        REQUIREMENT_HEADERS
    )

    if not start_match:

        return ""

    start_index = start_match.end()

    remaining = text[start_index:]

    stop_positions = []

    for header in STOP_HEADERS:

        normalized_remaining = (
            normalize_for_search(
                remaining
            )
        )

        normalized_header = (
            normalize_for_search(header)
        )

        pattern = re.compile(
            rf"\b{re.escape(normalized_header)}\b"
            rf"\s*(?::|-)?"
        )

        match = pattern.search(
            normalized_remaining
        )

        if match:

            stop_positions.append(
                match.start()
            )

    if stop_positions:

        end_index = min(
            stop_positions
        )

        return remaining[
            :end_index
        ].strip()

    return remaining.strip()


def split_requirement_statements(
    text: str
):

    if not text:
        return []

    # Normalize bullets.
    text = re.sub(
        r"[•▪◦]",
        "\n",
        text
    )

    # Normalize CR/LF.
    text = text.replace(
        "\r",
        "\n"
    )

    # Split on line breaks.
    parts = text.split("\n")

    statements = []

    for part in parts:

        part = part.strip()

        if not part:
            continue

        # If the PDF/JD produced multiple
        # requirements on one line, use
        # sentence boundaries.
        sentence_parts = re.split(
            r"(?<=[.!?])\s+(?=[A-Z])",
            part
        )

        for sentence in sentence_parts:

            sentence = sentence.strip()

            if len(sentence) >= 8:

                statements.append(
                    sentence
                )

    return statements


def get_priority(text: str):

    text_lower = normalize_for_search(
        text
    )

    for phrase in PREFERRED_PHRASES:

        if phrase in text_lower:

            return "PREFERRED"

    return "REQUIRED"


def is_any_of(text: str):

    text_lower = normalize_for_search(
        text
    )

    for pattern in ANY_OF_PATTERNS:

        if re.search(
            pattern,
            text_lower
        ):

            return True

    return False


def is_education_requirement(
    text: str
):

    text_lower = normalize_for_search(
        text
    )

    patterns = [
        "bachelor's degree",
        "bachelors degree",
        "bachelor degree",
        "master's degree",
        "masters degree",
        "phd",
        "degree completed",
        "degree in progress"
    ]

    return any(
        pattern in text_lower
        for pattern in patterns
    )


def is_language_requirement(
    text: str
):

    text_lower = normalize_for_search(
        text
    )

    patterns = [
        "fluency in english",
        "fluent in english",
        "english fluency",
        "native or bilingual",
        "native english",
        "bilingual level"
    ]

    return any(
        pattern in text_lower
        for pattern in patterns
    )


def is_writing_requirement(
    text: str
):

    text_lower = normalize_for_search(
        text
    )

    patterns = [
        "writing skills",
        "writing and grammar",
        "grammar skills",
        "excellent writing",
        "written communication"
    ]

    return any(
        pattern in text_lower
        for pattern in patterns
    )


def is_experience_requirement(
    text: str
):

    text_lower = normalize_for_search(
        text
    )

    patterns = [
        "previous experience as",
        "professional experience",
        "work experience",
        "relevant experience",
        "experience as a",
        "experience as an",
        "years of experience"
    ]

    return any(
        pattern in text_lower
        for pattern in patterns
    )


def classify_requirement(
    statement: str
):

    priority = get_priority(
        statement
    )

    # Education
    if is_education_requirement(
        statement
    ):

        return {
            "type": "EDUCATION",
            "priority": priority,
            "source_text": statement,
            "skills": []
        }

    # Language
    if is_language_requirement(
        statement
    ):

        return {
            "type": "LANGUAGE",
            "priority": priority,
            "source_text": statement,
            "skills": []
        }

    # Writing
    if is_writing_requirement(
        statement
    ):

        return {
            "type": "WRITING",
            "priority": priority,
            "source_text": statement,
            "skills": []
        }

    # Experience
    if is_experience_requirement(
        statement
    ):

        return {
            "type": "EXPERIENCE",
            "priority": priority,
            "source_text": statement,
            "skills": []
        }

    # Technical skills
    skill_dict = extract_skills(
        statement
    )

    skills = get_flat_skills(
        skill_dict
    )

    if skills:

        return {
            "type": (
                "ANY_OF"
                if is_any_of(statement)
                else "ALL_OF"
            ),
            "priority": priority,
            "source_text": statement,
            "skills": skills
        }

    return None


def extract_requirements(
    job_description: str
):

    requirement_section = (
        extract_requirement_section(
            job_description
        )
    )

    # IMPORTANT:
    # If a recognized qualification
    # section exists, do NOT fall back to
    # the entire JD.
    if requirement_section:

        statements = (
            split_requirement_statements(
                requirement_section
            )
        )

    else:

        # Fallback only when no section
        # heading exists anywhere.
        statements = (
            split_requirement_statements(
                job_description
            )
        )

    requirements = []

    for statement in statements:

        requirement = classify_requirement(
            statement
        )

        if requirement:

            requirements.append(
                requirement
            )

    return requirements