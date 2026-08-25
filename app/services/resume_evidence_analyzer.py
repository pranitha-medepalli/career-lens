import re


SECTION_PATTERNS = {

    "education": [
        "education",
        "academic background"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "skills": [
        "technical skills",
        "technicalskills",
        "skills",
        "core skills"
    ],

    "achievements": [
        "achievements",
        "certifications and achievements",
        "certificationsandachievements",
        "awards",
        "accomplishments",
        "honors"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses"
    ],

    "mentorship": [
        "mentorship",
        "mentoring"
    ],

    "leadership": [
        "leadership",
        "positions of responsibility",
        "activities",
        "volunteering",
        "volunteer"
    ],

    "interests": [
        "interests",
        "hobbies",
        "interests & hobbies",
        "interestsandhobbies",
        "extracurricular"
    ]
}


def normalize_text(text: str):

    text = text.replace("\r", "\n")

    text = re.sub(
        r"\n{2,}",
        "\n",
        text
    )

    return text.strip()


def normalize_heading(text: str):

    text = text.lower()

    text = text.replace("&", "and")

    text = re.sub(
        r"[^a-z0-9\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        "",
        text
    )

    return text


def find_section_positions(text: str):

    positions = []

    lines = text.split("\n")

    normalized_sections = {}

    for section, patterns in SECTION_PATTERNS.items():

        normalized_sections[section] = [
            normalize_heading(pattern)
            for pattern in patterns
        ]

    for index, line in enumerate(lines):

        cleaned_line = normalize_heading(
            line.strip()
        )

        for section, patterns in normalized_sections.items():

            if cleaned_line in patterns:

                positions.append({
                    "section": section,
                    "line_index": index
                })

                break

    return sorted(
        positions,
        key=lambda x: x["line_index"]
    )


def extract_sections(text: str):

    text = normalize_text(text)

    lines = text.split("\n")

    positions = find_section_positions(text)

    sections = {}

    for index, current in enumerate(positions):

        section_name = current["section"]

        start = current["line_index"] + 1

        if index + 1 < len(positions):

            end = positions[index + 1]["line_index"]

        else:

            end = len(lines)

        section_text = "\n".join(
            lines[start:end]
        ).strip()

        sections[section_name] = section_text

    return sections


def clean_bullet(line: str):

    return re.sub(
        r"^[•\-\*▪◦]\s*",
        "",
        line.strip()
    ).strip()


def split_lines(text: str):

    if not text:
        return []

    lines = text.split("\n")

    return [
        line.strip()
        for line in lines
        if line.strip()
    ]


def split_bullets(text: str):

    lines = split_lines(text)

    items = []

    for line in lines:

        cleaned = clean_bullet(line)

        if cleaned:

            items.append(cleaned)

    return items


def parse_projects(text: str):

    lines = split_lines(text)

    projects = []

    current_project = None

    for line in lines:

        cleaned = clean_bullet(line)

        if not cleaned:
            continue

        # A line without a bullet is considered
        # a potential project heading.

        is_bullet = bool(
            re.match(
                r"^[•\-\*▪◦]",
                line
            )
        )

        # Detect project titles based on common
        # technology / project formatting.

        looks_like_project_title = (

            not is_bullet

            and (
                "(" in line
                or
                line.lower().endswith("application")
                or
                line.lower().endswith("builder")
                or
                line.lower().endswith("dashboard")
            )
        )

        if looks_like_project_title:

            if current_project:

                projects.append(
                    current_project
                )

            title = line

            technologies = []

            tech_match = re.search(
                r"\((.*?)\)",
                line
            )

            if tech_match:

                tech_text = tech_match.group(1)

                technologies = [
                    tech.strip()
                    for tech in tech_text.split(",")
                ]

                title = re.sub(
                    r"\(.*?\)",
                    "",
                    line
                ).strip()

            title = re.sub(
                r"\s+Link$",
                "",
                title,
                flags=re.IGNORECASE
            ).strip()

            current_project = {

                "title": title,

                "technologies":
                    technologies,

                "evidence": []
            }

        else:

            if current_project:

                current_project[
                    "evidence"
                ].append(cleaned)

    if current_project:

        projects.append(
            current_project
        )

    return projects


def parse_interests(text: str):

    lines = split_lines(text)

    interests = []

    for line in lines:

        cleaned = clean_bullet(line)

        if cleaned:

            interests.append(cleaned)

    return interests


def parse_achievements(text: str):

    lines = split_lines(text)

    achievements = []

    for line in lines:

        cleaned = clean_bullet(line)

        if not cleaned:
            continue

        # Split common achievement separators.

        parts = re.split(
            r"\s*;\s*",
            cleaned
        )

        for part in parts:

            if part.strip():

                achievements.append(
                    part.strip()
                )

    return achievements


def analyze_education(text: str):

    items = split_bullets(text)

    degree_keywords = [

        "b.tech",
        "btech",
        "b.e",
        "bachelor",
        "b.sc",
        "master",
        "m.tech",
        "m.sc"
    ]

    degree_evidence = []

    for item in items:

        item_lower = item.lower()

        if any(
            keyword in item_lower
            for keyword in degree_keywords
        ):

            degree_evidence.append(item)

    return {

        "items": items,

        "degree_evidence":
            degree_evidence,

        "has_degree":
            bool(degree_evidence)
    }


def analyze_experience(text: str):

    items = split_bullets(text)

    return {

        "items": items,

        "has_experience":
            bool(items)
    }


def analyze_mentorship(text: str):

    items = split_bullets(text)

    return {

        "items": items,

        "has_mentorship":
            bool(items),

        "mentorship_count":
            len(items)
    }


def analyze_certifications(text: str):

    items = split_bullets(text)

    return {

        "items": items,

        "certification_count":
            len(items)
    }


def analyze_leadership(text: str):

    items = split_bullets(text)

    return {

        "items": items,

        "leadership_count":
            len(items)
    }


def analyze_resume_evidence(resume_text: str):

    sections = extract_sections(
        resume_text
    )

    education = analyze_education(
        sections.get(
            "education",
            ""
        )
    )

    experience = analyze_experience(
        sections.get(
            "experience",
            ""
        )
    )

    projects = parse_projects(
        sections.get(
            "projects",
            ""
        )
    )

    achievements = parse_achievements(
        sections.get(
            "achievements",
            ""
        )
    )

    certifications = analyze_certifications(
        sections.get(
            "certifications",
            ""
        )
    )

    mentorship = analyze_mentorship(
        sections.get(
            "mentorship",
            ""
        )
    )

    leadership = analyze_leadership(
        sections.get(
            "leadership",
            ""
        )
    )

    interests = parse_interests(
        sections.get(
            "interests",
            ""
        )
    )

    return {

        "sections": sections,

        "education": education,

        "experience": experience,

        "projects": {

            "items":
                projects,

            "project_count":
                len(projects)
        },

        "achievements": {

            "items":
                achievements,

            "achievement_count":
                len(achievements)
        },

        "certifications":
            certifications,

        "mentorship":
            mentorship,

        "leadership":
            leadership,

        "interests": {

            "items":
                interests,

            "interest_count":
                len(interests)
        }
    }