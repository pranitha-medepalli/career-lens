from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.services.file_parser import (
    extract_text_from_file
)

from app.services.resume_evidence_analyzer import (
    analyze_resume_evidence
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume Evidence Analysis"]
)


@router.post("/analyze")
async def analyze_resume_evidence_endpoint(
    file: UploadFile = File(...)
):

    try:

        resume_text = (
            await extract_text_from_file(
                file
            )
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume"
            )

        evidence = (
            analyze_resume_evidence(
                resume_text
            )
        )

        return {
            "filename":
                file.filename,

            "resume_evidence":
                evidence
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )