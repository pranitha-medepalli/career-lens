from fastapi import (
    APIRouter,
    HTTPException
)

from app.services.history_db import (
    get_all_job_analyses,
    get_job_analysis,
    delete_job_analysis
)


router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("")
def get_history():

    return {
        "history":
            get_all_job_analyses()
    }


@router.get("/{analysis_id}")
def get_history_item(
    analysis_id: int
):

    result = get_job_analysis(
        analysis_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return result


@router.delete("/{analysis_id}")
def remove_history_item(
    analysis_id: int
):

    deleted = delete_job_analysis(
        analysis_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return {
        "message":
            "Analysis deleted successfully."
    }