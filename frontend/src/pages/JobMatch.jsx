import { useState } from "react";
import API from "../services/api";


function JobMatch({ resumeFile }) {

  const [jobDescription, setJobDescription] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const analyzeJob = async () => {

    if (!resumeFile) {
      setError(
        "Please upload your resume first."
      );
      return;
    }

    if (!jobDescription.trim()) {
      setError(
        "Please paste a job description."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const formData = new FormData();

      formData.append(
        "file",
        resumeFile
      );

      formData.append(
        "job_description",
        jobDescription
      );

      const response = await API.post(
        "/job/match",
        formData
      );

      setResult(response.data);

    } catch (err) {

      console.error(
        "Job match error:",
        err
      );

      setError(
        err?.response?.data?.detail ||
        "Unable to analyze the job description."
      );

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="job-match-page">

      {/* =========================
          PAGE HEADER
      ========================= */}

      <div className="job-page-header">

        <div>

          <span className="eyebrow">
            JOB MATCH ANALYZER
          </span>

          <h2>
            Compare your resume with a job
          </h2>

          <p>
            See where you match, where you have
            gaps, and exactly what you can improve.
          </p>

        </div>

      </div>


      {/* =========================
          INPUT AREA
      ========================= */}

      <div className="job-match-grid">

        {/* Resume */}

        <div className="job-input-card resume-card">

          <div className="card-label">
            YOUR RESUME
          </div>

          <div className="resume-file-display">

            <div className="resume-file-icon">
              PDF
            </div>

            <div className="resume-file-info">

              <strong>
                {resumeFile
                  ? resumeFile.name
                  : "No resume selected"}
              </strong>

              <span>
                Ready for analysis
              </span>

            </div>

            <div className="check-icon">
              ✓
            </div>

          </div>

          <div className="resume-card-note">

            Your uploaded resume will be compared
            directly against the job description.

          </div>

        </div>


        {/* Job Description */}

        <div className="job-input-card">

          <div className="card-label">
            JOB DESCRIPTION
          </div>

          <textarea
            className="job-description-input"
            value={jobDescription}
            onChange={(event) =>
              setJobDescription(
                event.target.value
              )
            }
            placeholder="Paste the complete job description here..."
          />

          <div className="character-count">
            {jobDescription.length} characters
          </div>

        </div>

      </div>


      {/* =========================
          ERROR
      ========================= */}

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {/* =========================
          ANALYZE
      ========================= */}

      <button
        className="analyze-job-button"
        onClick={analyzeJob}
        disabled={loading}
      >

        {loading ? (
          <>
            <span className="loading-dot" />
            Analyzing Job...
          </>
        ) : (
          <>
            Analyze Job Match
            <span className="button-arrow">
              →
            </span>
          </>
        )}

      </button>


      {/* =========================
          RESULTS
      ========================= */}

      {result && (
        <MatchResults
          result={result}
        />
      )}

    </div>
  );
}


/* =================================================
   MATCH RESULTS
================================================= */

function MatchResults({ result }) {

  const score =
    result.overall_match_score || 0;

  let scoreLabel =
    "Needs Improvement";

  if (score >= 80) {

    scoreLabel =
      "Strong Match";

  } else if (score >= 60) {

    scoreLabel =
      "Good Match";
  }


  return (
    <div className="match-results">

      {/* =========================
          SCORE
      ========================= */}

      <section className="match-overview">

        <div className="match-score-panel">

          <span className="eyebrow">
            OVERALL MATCH
          </span>

          <div className="score-number">
            {score}%
          </div>

          <h3>
            {scoreLabel}
          </h3>

          <p>
            Based on your skills, education,
            project evidence, and job requirements.
          </p>

        </div>


        <div className="match-summary-panel">

          <div className="summary-item">

            <strong>
              {
                result.matching_summary
                  ?.strong_matches || 0
              }
            </strong>

            <span>
              Strong Matches
            </span>

          </div>


          <div className="summary-item">

            <strong>
              {
                result.matching_summary
                  ?.partial_matches || 0
              }
            </strong>

            <span>
              Partial Matches
            </span>

          </div>


          <div className="summary-item">

            <strong>
              {
                result.matching_summary
                  ?.not_verifiable || 0
              }
            </strong>

            <span>
              Not Verifiable
            </span>

          </div>

        </div>

      </section>


      {/* =========================
          REQUIREMENTS
      ========================= */}

      <section className="job-result-section">

        <div className="section-title">

          <span className="eyebrow">
            REQUIREMENT ANALYSIS
          </span>

          <h2>
            How your resume matches
          </h2>

        </div>


        <div className="requirement-list">

          {result.requirement_analysis?.map(
            (requirement, index) => (

              <RequirementCard
                key={index}
                requirement={requirement}
              />

            )
          )}

        </div>

      </section>


      {/* =========================
          IMPROVEMENTS
      ========================= */}

      {result.resume_improvements && (

        <section className="job-result-section">

          <div className="section-title">

            <span className="eyebrow">
              RESUME IMPROVEMENTS
            </span>

            <h2>
              What should you change?
            </h2>

          </div>


          <div className="improvement-list">

            {result
              .resume_improvements
              ?.improvements
              ?.map(
                (item, index) => (

                  <ImprovementCard
                    key={index}
                    item={item}
                  />

                )
              )}

          </div>

        </section>

      )}


      {/* =========================
          BULLET OPTIMIZER
      ========================= */}

      {result.bullet_optimizations?.length > 0 && (

        <section className="job-result-section">

          <div className="section-title">

            <span className="eyebrow">
              BULLET OPTIMIZER
            </span>

            <h2>
              Improve your resume bullets
            </h2>

          </div>


          <div className="bullet-list">

            {result.bullet_optimizations.map(
              (item, index) => (

                <BulletCard
                  key={index}
                  item={item}
                />

              )
            )}

          </div>

        </section>

      )}

    </div>
  );
}


/* =================================================
   REQUIREMENT CARD
================================================= */

function RequirementCard({
  requirement
}) {

  let statusClass =
    "status-neutral";

  if (
    requirement.status ===
    "STRONG_MATCH"
  ) {

    statusClass =
      "status-success";

  } else if (
    requirement.status ===
    "PARTIAL_MATCH"
  ) {

    statusClass =
      "status-warning";
  }


  const displayStatus = (
    requirement.status || "UNKNOWN"
  ).replaceAll(
    "_",
    " "
  );


  return (
    <div className="requirement-card">

      <div className="requirement-card-header">

        <div>

          <span className="requirement-type">
            {requirement.type}
          </span>

          <h3>
            {requirement.requirement}
          </h3>

        </div>

        <span
          className={`status-pill ${statusClass}`}
        >
          {displayStatus}
        </span>

      </div>


      {requirement.matched_skills?.length > 0 && (

        <div className="tag-container">

          {requirement.matched_skills.map(
            (skill) => (

              <span
                className="tag tag-success"
                key={skill}
              >
                {skill}
              </span>

            )
          )}

        </div>

      )}


      {requirement.missing_skills?.length > 0 && (

        <div className="tag-container">

          {requirement.missing_skills.map(
            (skill) => (

              <span
                className="tag tag-warning"
                key={`missing-${skill}`}
              >
                {skill}
              </span>

            )
          )}

        </div>

      )}


      <div className="requirement-footer">

        <span>
          Confidence
        </span>

        <strong>
          {requirement.confidence}%
        </strong>

      </div>


      {requirement.recommendation && (

        <p className="recommendation">
          {requirement.recommendation}
        </p>

      )}

    </div>
  );
}


/* =================================================
   IMPROVEMENT CARD
================================================= */

function ImprovementCard({
  item
}) {

  return (
    <div className="improvement-card">

      <div className="improvement-meta">

        <span
          className={`priority-badge ${
            (
              item.priority || "LOW"
            ).toLowerCase()
          }`}
        >
          {item.priority}
        </span>

        <span className="action-badge">
          {item.action}
        </span>

      </div>


      <h3>
        {item.requirement}
      </h3>


      <p>
        {item.message}
      </p>

    </div>
  );
}


/* =================================================
   BULLET CARD
================================================= */

function BulletCard({
  item
}) {

  const copyBullet = async () => {

    try {

      await navigator.clipboard.writeText(
        item.suggested_bullet
      );

      alert(
        "Suggested bullet copied."
      );

    } catch {

      alert(
        "Unable to copy suggestion."
      );

    }

  };


  return (
    <div className="bullet-card">

      <div className="project-heading">

        <span className="project-label">
          PROJECT
        </span>

        <h3>
          {item.project}
        </h3>

      </div>


      <div className="bullet-comparison">

        <div className="bullet-panel">

          <span>
            CURRENT
          </span>

          <p>
            {item.original_bullet}
          </p>

        </div>


        <div className="bullet-panel suggested">

          <span>
            SUGGESTED
          </span>

          <p>
            {item.suggested_bullet}
          </p>

          <button
            className="copy-button"
            onClick={copyBullet}
          >
            Copy suggestion
          </button>

        </div>

      </div>


      <div className="bullet-reason">

        <strong>
          Why change this?
        </strong>

        <p>
          {item.reason}
        </p>

      </div>

    </div>
  );
}


export default JobMatch;