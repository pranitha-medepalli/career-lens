def find_project_from_evidence(
    resume_evidence,
    evidence_item
):
    projects = (
        resume_evidence
        .get("projects", {})
        .get("items", [])
    )

    evidence_text = (
        evidence_item.get("text", "")
        .strip()
        .lower()
    )

    for project in projects:

        title = project.get(
            "title",
            ""
        ).strip()

        title_lower = title.lower()

        # --------------------------------
        # Evidence refers to project title
        # --------------------------------

        if evidence_text == title_lower:

            return project

        # --------------------------------
        # Evidence refers to a project
        # bullet
        # --------------------------------

        for bullet in project.get(
            "evidence",
            []
        ):

            if (
                evidence_text
                == bullet.strip().lower()
            ):

                return project

    return None


def create_optimized_bullet(
    project,
    original_bullet
):
    title = project.get(
        "title",
        "project"
    )

    technologies = project.get(
        "technologies",
        []
    )

    # Avoid repeating technologies if the
    # original bullet already mentions them.

    original_lower = (
        original_bullet.lower()
    )

    missing_technologies = [

        technology

        for technology in technologies

        if technology.lower()
        not in original_lower
    ]

    technology_phrase = ""

    if missing_technologies:

        technology_phrase = (
            " using "
            + ", ".join(
                missing_technologies
            )
        )

    # We are only restructuring information
    # already present in the resume.
    optimized_bullet = (
        original_bullet.rstrip(".")
        + technology_phrase
        + "."
    )

    return {

        "project":
            title,

        "original_bullet":
            original_bullet,

        "suggested_bullet":
            optimized_bullet,

        "reason":
            (
                "The suggestion strengthens the "
                "existing bullet by making relevant "
                "technologies more visible without "
                "inventing new experience."
            )
    }


def generate_bullet_optimizations(
    resume_evidence,
    requirement_results
):

    optimizations = []

    seen_projects = set()

    for result in requirement_results:

        if result.get("status") != "PARTIAL_MATCH":
            continue

        for evidence in result.get(
            "evidence",
            []
        ):

            source = evidence.get(
                "source",
                ""
            )

            if source not in (
                "project",
                "project_title"
            ):
                continue

            project = find_project_from_evidence(
                resume_evidence,
                evidence
            )

            if not project:
                continue

            project_title = project.get(
                "title",
                ""
            )

            # Don't generate several duplicate
            # optimizations for the same project.

            if project_title in seen_projects:
                continue

            seen_projects.add(
                project_title
            )

            project_bullets = project.get(
                "evidence",
                []
            )

            if not project_bullets:
                continue

            # Choose the first meaningful bullet.
            original_bullet = project_bullets[0]

            optimization = (
                create_optimized_bullet(
                    project,
                    original_bullet
                )
            )

            optimizations.append(
                optimization
            )

    return optimizations