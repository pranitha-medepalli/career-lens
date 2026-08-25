from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.resume import (
    router as resume_router
)

from app.api.resume_analysis import (
    router as resume_analysis_router
)

from app.api.job_match import (
    router as job_match_router
)

from app.api.history import (
    router as history_router
)

from app.services.history_db import (
    initialize_database
)


app = FastAPI(
    title="AI Career Copilot",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


initialize_database()


app.include_router(
    resume_router
)

app.include_router(
    resume_analysis_router
)

app.include_router(
    job_match_router
)

app.include_router(
    history_router
)


@app.get("/")
def root():

    return {
        "message":
            "AI Career Copilot API is running"
    }