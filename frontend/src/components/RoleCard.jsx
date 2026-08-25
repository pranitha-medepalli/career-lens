import React from "react";

function RoleCard({ role, rank }) {
  const score = role.match_score;

  const scoreClass =
    score >= 80
      ? "score-high"
      : score >= 60
      ? "score-medium"
      : "score-low";

  return (
    <div className="role-card">
      <div className="role-header">
        <div className="role-rank">
          #{rank}
        </div>

        <div className="role-title">
          <h3>{role.role}</h3>
          <span>
            {role.confidence} confidence
          </span>
        </div>

        <div
          className={`role-score ${scoreClass}`}
        >
          {score}%
        </div>
      </div>

      <p className="role-description">
        {role.description}
      </p>

      <div className="role-section">
        <h4>Matching Skills</h4>

        <div className="tag-container">
          {role.matching_skills.map(
            (item) => (
              <span
                className="tag tag-success"
                key={`${role.role}-${item.skill}`}
              >
                {item.skill}
              </span>
            )
          )}
        </div>
      </div>

      {role.skill_gaps?.length > 0 && (
        <div className="role-section">
          <h4>Skill Gaps</h4>

          <div className="tag-container">
            {role.skill_gaps.map(
              (skill) => (
                <span
                  className="tag tag-warning"
                  key={`${role.role}-${skill}`}
                >
                  {skill}
                </span>
              )
            )}
          </div>
        </div>
      )}

      <div className="role-section">
        <h4>Why This Role?</h4>

        <p>
          {role.why_this_role}
        </p>
      </div>

      <div className="role-section">
        <h4>Next Steps</h4>

        <ul className="next-step-list">
          {role.next_steps
            .slice(0, 3)
            .map((step) => (
              <li key={step}>
                {step}
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
}

export default RoleCard;