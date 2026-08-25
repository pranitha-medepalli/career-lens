function Dashboard({
  analysis
}) {

  const topRole =
    analysis?.suggested_roles?.[0];

  const skillCount =
    Object.values(
      analysis?.skills || {}
    )
      .flat()
      .length;

  return (
    <div>

      <div className="dashboard-header">

        <div>
          <span className="eyebrow">
            DASHBOARD
          </span>

          <h2>
            Your Career Snapshot
          </h2>

          <p>
            A quick overview of your resume
            and career direction.
          </p>
        </div>

      </div>


      <section className="stats-grid">

        <div className="stat-card">

          <span>
            Top Career Match
          </span>

          <strong>
            {topRole?.role || "—"}
          </strong>

          <small>
            {topRole?.match_score || 0}%
            match
          </small>

        </div>


        <div className="stat-card">

          <span>
            Skills Identified
          </span>

          <strong>
            {skillCount}
          </strong>

          <small>
            Across your resume
          </small>

        </div>


        <div className="stat-card">

          <span>
            Roles Recommended
          </span>

          <strong>
            {analysis
              ?.suggested_roles
              ?.length || 0}
          </strong>

          <small>
            Based on your profile
          </small>

        </div>

      </section>

    </div>
  );
}

export default Dashboard;
