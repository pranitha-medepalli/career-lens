import re

from app.data.skills import SKILLS


SKILL_ALIASES = {
    "nextjs": "next.js",
    "next js": "next.js",

    "nodejs": "node.js",
    "node js": "node.js",

    "restful api": "rest api",
    "restful apis": "rest api",
    "rest api": "rest api",
    "rest apis": "rest api",

    "postgres": "postgresql",

    "google cloud": "gcp",

    "large language model": "llm",
    "large language models": "llm",

    "github": "git",
    "github.com": "git"
}


def normalize_skill(skill: str) -> str:

    skill = skill.lower().strip()

    return SKILL_ALIASES.get(
        skill,
        skill
    )


def skill_exists_in_text(
    skill: str,
    text: str
) -> bool:

    skill = skill.lower()

    # Special handling for short skills
    if skill == "c":
        pattern = r"(?<![a-zA-Z])C(?![a-zA-Z])"
        return bool(
            re.search(
                pattern,
                text,
                re.IGNORECASE
            )
        )

    pattern = (
        r"(?<!\w)"
        + re.escape(skill)
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            text,
            re.IGNORECASE
        )
    )


def extract_skills(text: str):

    found_skills = {}

    for category, skills in SKILLS.items():

        category_skills = []

        for skill in skills:

            if skill_exists_in_text(
                skill,
                text
            ):

                normalized = normalize_skill(skill)

                if (
                    normalized
                    not in category_skills
                ):

                    category_skills.append(
                        normalized
                    )

        if category_skills:

            found_skills[category] = (
                category_skills
            )

    return found_skills


def get_flat_skills(skill_dict):

    skills = []

    for category_skills in skill_dict.values():

        skills.extend(
            category_skills
        )

    return sorted(
        list(set(skills))
    )