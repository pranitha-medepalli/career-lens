import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Career Copilot",
    version="1.0.0"
)


frontend_url = os.getenv(
    "FRONTEND_URL",
    "https://pranitha-medepalli.github.io/career-lens/"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        frontend_url
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)