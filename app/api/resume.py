from fastapi import (
    APIRouter,
    UploadFile,
    File,
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

from app.services.career_role_engine import (
    suggest_career_roles
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/role-analysis")
async def analyze_resume_roles(
    file: UploadFile = File(...)
):

    try:

        # =================================
        # Extract resume text
        # =================================

        resume_text = (
            await extract_text_from_file(
                file
            )
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text "
                    "from resume."
                )
            )

        # =================================
        # Extract technical skills
        # =================================

        skill_categories = (
            extract_skills(
                resume_text
            )
        )

        flat_skills = (
            get_flat_skills(
                skill_categories
            )
        )

        # =================================
        # Extract structured evidence
        # =================================

        resume_evidence = (
            analyze_resume_evidence(
                resume_text
            )
        )

        # =================================
        # Career role engine
        # =================================

        suggested_roles = (
            suggest_career_roles(

                resume_evidence,

                skill_categories,

                top_n=5
            )
        )

        # =================================
        # Response
        # =================================

        return {

            "filename":
                file.filename,

            "skills":
                skill_categories,

            "suggested_roles":
                suggested_roles
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )