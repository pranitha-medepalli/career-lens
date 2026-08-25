from typing import Dict, List, Set, Any


# ============================================================
# ROLE DEFINITIONS
# ============================================================

ROLE_PROFILES = {

    "Backend Developer": {

        "description":
            "Builds APIs, backend services, databases, and server-side applications.",

        "skills": {

            "python": 15,
            "java": 15,
            "node.js": 15,

            "fastapi": 12,
            "flask": 10,
            "django": 10,
            "spring boot": 12,
            "express": 10,

            "sql": 10,
            "postgresql": 8,
            "mysql": 8,
            "mongodb": 6,

            "rest api": 12,
            "docker": 8,
            "git": 5
        },

        "evidence_types": [
            "project",
            "project_technologies",
            "mentorship"
        ],

        "next_steps": [
            "Build a production-style REST API.",
            "Strengthen database design and PostgreSQL.",
            "Learn backend deployment and cloud hosting.",
            "Add automated testing and CI/CD to a backend project."
        ]
    },

    "Full Stack Developer": {

        "description":
            "Develops complete web applications across frontend and backend.",

        "skills": {

            "javascript": 12,
            "typescript": 12,
            "react": 15,
            "html": 7,
            "css": 7,

            "node.js": 12,
            "express": 8,

            "python": 7,
            "sql": 8,
            "mongodb": 8,

            "rest api": 10,
            "git": 5,
            "docker": 5
        },

        "evidence_types": [
            "project",
            "project_technologies"
        ],

        "next_steps": [
            "Build and deploy a complete full-stack application.",
            "Strengthen API design and authentication.",
            "Add testing and CI/CD.",
            "Deploy a frontend and backend together."
        ]
    },

    "Software Engineer": {

        "description":
            "Designs, develops, tests, and maintains software applications.",

        "skills": {

            "python": 10,
            "java": 10,
            "javascript": 10,
            "typescript": 8,
            "c": 8,
            "c++": 8,

            "sql": 8,
            "git": 8,

            "data structures": 12,
            "algorithms": 12,
            "oop": 8,

            "docker": 5
        },

        "evidence_types": [
            "project",
            "mentorship",
            "achievement"
        ],

        "next_steps": [
            "Strengthen system design fundamentals.",
            "Continue DSA and coding problem practice.",
            "Build a production-quality software project.",
            "Add testing, debugging, and CI/CD experience."
        ]
    },

    "Frontend Developer": {

        "description":
            "Builds responsive and interactive user interfaces.",

        "skills": {

            "javascript": 15,
            "typescript": 15,
            "react": 20,
            "html": 10,
            "css": 10,

            "tailwind": 8,
            "next.js": 8,
            "vite": 8,

            "git": 5
        },

        "evidence_types": [
            "project",
            "project_technologies"
        ],

        "next_steps": [
            "Build a polished production-style React application.",
            "Strengthen accessibility and responsive design.",
            "Learn advanced React patterns and state management.",
            "Deploy frontend applications independently."
        ]
    },

    "AI Application Developer": {

        "description":
            "Builds applications using AI, LLMs, APIs, and intelligent workflows.",

        "skills": {

            "python": 15,
            "openai": 18,
            "llm": 15,
            "rag": 12,
            "langchain": 10,

            "machine learning": 10,
            "react": 6,
            "node.js": 6,

            "rest api": 8,
            "docker": 6,
            "git": 4
        },

        "evidence_types": [
            "project",
            "project_technologies",
            "achievement"
        ],

        "next_steps": [
            "Build an end-to-end LLM application.",
            "Learn RAG and vector databases.",
            "Add evaluation and hallucination testing.",
            "Deploy an AI application with monitoring."
        ]
    },

    "DevOps Engineer": {

        "description":
            "Automates software delivery, deployment, infrastructure, and operations.",

        "skills": {

            "docker": 18,
            "kubernetes": 18,
            "aws": 12,
            "azure": 12,
            "gcp": 10,

            "linux": 10,
            "terraform": 10,

            "ci/cd": 10,
            "github actions": 8,
            "jenkins": 8,

            "git": 8
        },

        "evidence_types": [
            "project_technologies",
            "project"
        ],

        "next_steps": [
            "Learn one major cloud platform.",
            "Build a CI/CD pipeline.",
            "Deploy a containerized application.",
            "Learn infrastructure as code with Terraform."
        ]
    },

    "AI Engineer": {

        "description":
            "Develops machine-learning and AI systems and production AI solutions.",

        "skills": {

            "python": 15,
            "machine learning": 18,
            "deep learning": 12,
            "llm": 12,

            "rag": 10,
            "langchain": 8,
            "vector database": 8,

            "openai": 10,
            "docker": 7,

            "sql": 5
        },

        "evidence_types": [
            "project",
            "project_technologies",
            "achievement"
        ],

        "next_steps": [
            "Strengthen machine learning fundamentals.",
            "Build an end-to-end ML or LLM project.",
            "Learn model evaluation and deployment.",
            "Learn RAG, vector databases, and AI observability."
        ]
    }
}


# ============================================================
# RESUME DATA EXTRACTION
# ============================================================

def extract_resume_data(
    resume_evidence: dict,
    resume_skill_categories: dict | None = None
):

    skills = set()

    # --------------------------------
    # Skills from Technical Skills
    # --------------------------------

    if resume_skill_categories:

        for category_skills in (
            resume_skill_categories.values()
        ):

            for skill in category_skills:

                skills.add(
                    skill.lower().strip()
                )

    # --------------------------------
    # Structured project data
    # --------------------------------

    projects = (
        resume_evidence
        .get("projects", {})
        .get("items", [])
    )

    project_evidence = []

    for project in projects:

        # Project title
        title = project.get(
            "title",
            ""
        )

        if title:

            project_evidence.append(
                title
            )

        # Project technologies
        for technology in project.get(
            "technologies",
            []
        ):

            technology_clean = (
                technology.strip()
            )

            if technology_clean:

                skills.add(
                    technology_clean.lower()
                )

                # IMPORTANT:
                # Store technologies as evidence
                # so role recommendations can show
                # where the match came from.

                project_evidence.append(
                    technology_clean
                )

        # Project descriptions
        for item in project.get(
            "evidence",
            []
        ):

            project_evidence.append(
                item
            )

    # --------------------------------
    # Mentorship
    # --------------------------------

    mentorship = (
        resume_evidence
        .get("mentorship", {})
        .get("items", [])
    )

    # --------------------------------
    # Achievements
    # --------------------------------

    achievements = (
        resume_evidence
        .get("achievements", {})
        .get("items", [])
    )

    return {

        "skills":
            skills,

        "project_evidence":
            project_evidence,

        "mentorship":
            mentorship,

        "achievements":
            achievements
    }

# ============================================================
# ROLE MATCHING
# ============================================================

def calculate_role_match(
    role_name: str,
    profile: dict,
    resume_data: dict
):

    role_skills = profile["skills"]

    resume_skills = resume_data["skills"]

    total_possible_points = sum(
        role_skills.values()
    )

    earned_points = 0

    matching_skills = []

    missing_skills = []

    for skill, weight in role_skills.items():

        skill_lower = skill.lower()

        # Exact match
        if skill_lower in resume_skills:

            earned_points += weight

            matching_skills.append({
                "skill": skill,
                "weight": weight,
                "match_type": "EXACT"
            })

            continue

        # Related/alias matching
        related = get_related_skills(
            skill_lower
        )

        related_match = None

        for related_skill in related:

            if related_skill in resume_skills:

                related_match = related_skill

                break

        if related_match:

            earned_points += (
                weight * 0.7
            )

            matching_skills.append({

                "skill": skill,

                "matched_with":
                    related_match,

                "weight": weight,

                "match_type":
                    "RELATED"
            })

        else:

            missing_skills.append({
                "skill": skill,
                "weight": weight
            })

    if total_possible_points == 0:

        score = 0

    else:

        score = round(

            earned_points
            /
            total_possible_points
            * 100,

            2
        )

    return {

        "score": score,

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills
    }


# ============================================================
# RELATED SKILLS
# ============================================================

def get_related_skills(
    skill: str
):

    aliases = {

        "rest api": [
            "restful api",
            "rest apis"
        ],

        "postgresql": [
            "postgres"
        ],

        "mongodb": [
            "mongo"
        ],

        "javascript": [
            "js"
        ],

        "typescript": [
            "ts"
        ],

        "node.js": [
            "nodejs",
            "node"
        ],

        "next.js": [
            "nextjs"
        ],

        "machine learning": [
            "ml"
        ],

        "llm": [
            "large language model"
        ],

        "openai": [
            "openai api"
        ],

        "data structures": [
            "data structures & algorithms"
        ],

        "algorithms": [
            "data structures & algorithms"
        ],

        "oop": [
            "object oriented programming",
            "object-oriented programming"
        ]
    }

    return aliases.get(
        skill,
        []
    )

# ============================================================
# EVIDENCE ANALYSIS
# ============================================================

def collect_role_evidence(
    role_name: str,
    profile: dict,
    resume_data: dict
):

    evidence = []

    project_text = " ".join(
        resume_data["project_evidence"]
    ).lower()

    role_skills = profile["skills"]

    # --------------------------------
    # Project evidence
    # --------------------------------

    for skill in role_skills:

        skill_lower = skill.lower()

        if skill_lower not in project_text:
            continue

        for item in resume_data[
            "project_evidence"
        ]:

            if skill_lower in item.lower():

                evidence.append({

                    "source":
                        "project",

                    "skill":
                        skill,

                    "text":
                        item
                })

    # --------------------------------
    # Mentorship evidence
    # --------------------------------

    if role_name in (
        "Software Engineer",
        "Backend Developer"
    ):

        for item in resume_data[
            "mentorship"
        ]:

            evidence.append({

                "source":
                    "mentorship",

                "text":
                    item
            })

    # --------------------------------
    # AI evidence
    # --------------------------------

    if role_name in (
        "AI Engineer",
        "AI Application Developer"
    ):

        for item in resume_data[
            "achievements"
        ]:

            if (
                "machine learning"
                in item.lower()
                or
                "ai"
                in item.lower()
            ):

                evidence.append({

                    "source":
                        "achievement",

                    "text":
                        item
                })

    # --------------------------------
    # Remove duplicates
    # --------------------------------

    unique_evidence = []

    seen = set()

    for item in evidence:

        key = (
            item.get("source", ""),
            item.get("skill", ""),
            item.get("text", "")
        )

        if key in seen:
            continue

        seen.add(key)

        unique_evidence.append(item)

    return unique_evidence[:10]

# ============================================================
# CONFIDENCE
# ============================================================

def get_confidence(
    score: float
):

    if score >= 80:

        return "HIGH"

    if score >= 60:

        return "MEDIUM"

    return "LOW"


# ============================================================
# MAIN CAREER ROLE ENGINE
# ============================================================

def suggest_career_roles(
    resume_evidence: dict,
    resume_skill_categories: dict | None = None,
    top_n: int = 5
):

    resume_data = extract_resume_data(

        resume_evidence,

        resume_skill_categories
    )

    results = []

    for role_name, profile in (
        ROLE_PROFILES.items()
    ):

        match = calculate_role_match(

            role_name,

            profile,

            resume_data
        )

        evidence = collect_role_evidence(

            role_name,

            profile,

            resume_data
        )

        confidence = get_confidence(
            match["score"]
        )

        matching_skills = [

            item

            for item in match[
                "matching_skills"
            ]
        ]

        missing_skills = [

            item["skill"]

            for item in match[
                "missing_skills"
            ]
        ]

        # --------------------------------
        # Remove extremely low-value gaps
        # --------------------------------

        important_gaps = [

            item["skill"]

            for item in match[
                "missing_skills"
            ]

            if item["weight"] >= 8
        ]

        if not important_gaps:

            important_gaps = missing_skills[
                :5
            ]

        # --------------------------------
        # Generate explanation
        # --------------------------------

        if match["score"] >= 80:

            why_this_role = (
                f"Strong alignment with the "
                f"{role_name} skill profile."
            )

        elif match["score"] >= 60:

            why_this_role = (
                f"Good foundation for "
                f"{role_name}, with some "
                f"important skill gaps."
            )

        elif match["score"] >= 40:

            why_this_role = (
                f"Some relevant skills are "
                f"present, but significant "
                f"development is needed for "
                f"{role_name}."
            )

        else:

            why_this_role = (
                f"Limited alignment with the "
                f"current {role_name} profile."
            )

        results.append({

            "role":
                role_name,

            "match_score":
                match["score"],

            "confidence":
                confidence,

            "description":
                profile["description"],

            "matching_skills":
                matching_skills,

            "skill_gaps":
                important_gaps,

            "evidence":
                evidence,

            "why_this_role":
                why_this_role,

            "next_steps":
                profile["next_steps"]
        })

    # Highest score first.

    results.sort(

        key=lambda item:
            item["match_score"],

        reverse=True
    )

    return results[:top_n]