from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

from app.services.file_parser import (
    extract_text_from_file
)

from app.services.skill_extractor import (
    extract_skills,
    get_flat_skills
)

from app.services.resume_evidence_analyzer import (
    analyze_resume_evidence
)

from app.services.job_requirement_analyzer import (
    extract_requirements
)

from app.services.requirement_evidence_matcher import (
    match_requirements_with_resume
)

from app.services.resume_improvement_engine import (
    generate_resume_improvements
)

from app.services.bullet_optimizer import (
    generate_bullet_optimizations
)

from app.services.history_db import (
    save_job_analysis
)


router = APIRouter(
    prefix="/job",
    tags=["Job Matching"]
)


def calculate_overall_score(
    requirement_results
):
    """
    Calculate the overall job-match score.

    REQUIRED requirements:
        weight = 1.0

    PREFERRED requirements:
        weight = 0.4

    NOT_VERIFIABLE requirements:
        excluded from the score because
        absence of evidence is not proof
        that the candidate lacks the ability.
    """

    if not requirement_results:
        return 0

    weighted_score = 0
    total_weight = 0

    for result in requirement_results:

        status = result.get(
            "status",
            ""
        )

        # Do not penalize something that
        # cannot reasonably be verified
        # from a resume.
        if status == "NOT_VERIFIABLE":
            continue

        confidence = result.get(
            "confidence",
            0
        )

        priority = result.get(
            "priority",
            "REQUIRED"
        )

        if priority == "REQUIRED":
            weight = 1.0
        else:
            weight = 0.4

        weighted_score += (
            confidence * weight
        )

        total_weight += weight

    if total_weight == 0:
        return 0

    return round(
        weighted_score / total_weight,
        2
    )


@router.post("/match")
async def match_resume_with_job(

    file: UploadFile = File(...),

    job_description: str = Form(...)

):

    try:

        # =====================================
        # 1. Validate job description
        # =====================================

        if not job_description.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Job description "
                    "cannot be empty."
                )
            )

        # =====================================
        # 2. Extract resume text
        # =====================================

        resume_text = (
            await extract_text_from_file(
                file
            )
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract "
                    "text from the resume."
                )
            )

        # =====================================
        # 3. Extract resume skills
        # =====================================

        resume_skill_dict = (
            extract_skills(
                resume_text
            )
        )

        resume_skills = set(
            get_flat_skills(
                resume_skill_dict
            )
        )

        # =====================================
        # 4. Analyze structured resume evidence
        # =====================================

        resume_evidence = (
            analyze_resume_evidence(
                resume_text
            )
        )

        # =====================================
        # Add skill categories to evidence
        #
        # This lets the evidence matcher
        # access the resume's technical skills.
        # =====================================

        resume_evidence[
            "skill_categories"
        ] = resume_skill_dict

        # =====================================
        # 5. Extract job requirements
        # =====================================

        requirements = (
            extract_requirements(
                job_description
            )
        )

        # =====================================
        # 6. Match requirements against resume
        # =====================================

        evidence_matching = (
            match_requirements_with_resume(

                requirements,

                resume_evidence
            )
        )

        requirement_results = (
            evidence_matching.get(
                "requirements",
                []
            )
        )

        # =====================================
        # 7. Calculate overall score
        # =====================================

        overall_score = (
            calculate_overall_score(
                requirement_results
            )
        )

        # =====================================
        # 8. Generate resume improvements
        # =====================================

        resume_improvements = (
            generate_resume_improvements(

                requirements,

                requirement_results
            )
        )

        # =====================================
        # 9. Generate bullet optimizations
        # =====================================

        bullet_optimizations = (
            generate_bullet_optimizations(

                resume_evidence,

                requirement_results
            )
        )

        # =====================================
        # 10. Build complete analysis result
        # =====================================

        analysis_result = {

            "overall_match_score":
                overall_score,

            "resume": {

                "filename":
                    file.filename,

                "skills":
                    sorted(
                        list(resume_skills)
                    ),

                "skill_categories":
                    resume_skill_dict
            },

            "resume_evidence":
                resume_evidence,

            "job_description": {

                "requirements_detected":
                    len(requirements)
            },

            "matching_summary":
                evidence_matching.get(
                    "summary",
                    {}
                ),

            "requirement_analysis":
                requirement_results,

            "resume_improvements":
                resume_improvements,

            "bullet_optimizations":
                bullet_optimizations
        }

        # =====================================
        # 11. Save analysis to SQLite
        # =====================================

        history_id = save_job_analysis(

            resume_filename=
                file.filename,

            job_description=
                job_description,

            overall_match_score=
                overall_score,

            analysis_result=
                analysis_result
        )

        # =====================================
        # 12. Add history ID to response
        # =====================================

        analysis_result[
            "history_id"
        ] = history_id

        # =====================================
        # 13. Return final response
        # =====================================

        return analysis_result

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )