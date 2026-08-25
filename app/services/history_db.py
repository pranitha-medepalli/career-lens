import sqlite3
import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "career_copilot.db"


def get_connection():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume_filename TEXT NOT NULL,

            job_description TEXT NOT NULL,

            overall_match_score REAL NOT NULL,

            analysis_json TEXT NOT NULL,

            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


def save_job_analysis(
    resume_filename: str,
    job_description: str,
    overall_match_score: float,
    analysis_result: dict
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    cursor.execute(
        """
        INSERT INTO job_analyses
        (
            resume_filename,
            job_description,
            overall_match_score,
            analysis_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            resume_filename,
            job_description,
            overall_match_score,
            json.dumps(
                analysis_result
            ),
            created_at
        )
    )

    analysis_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return analysis_id


def get_all_job_analyses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            resume_filename,
            overall_match_score,
            created_at
        FROM job_analyses
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def get_job_analysis(
    analysis_id: int
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM job_analyses
        WHERE id = ?
        """,
        (analysis_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return None

    result = dict(row)

    result["analysis_json"] = json.loads(
        result["analysis_json"]
    )

    return result


def delete_job_analysis(
    analysis_id: int
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM job_analyses
        WHERE id = ?
        """,
        (analysis_id,)
    )

    deleted = (
        cursor.rowcount > 0
    )

    connection.commit()

    connection.close()

    return deleted