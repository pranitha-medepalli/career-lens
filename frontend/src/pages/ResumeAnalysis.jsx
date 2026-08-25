import SkillCard from "../components/SkillCard";

function ResumeAnalysis({
  analysis
}) {

  return (
    <div>

      <div className="dashboard-header">

        <div>

          <span className="eyebrow">
            RESUME ANALYSIS
          </span>

          <h2>
            Your Resume Profile
          </h2>

          <p>
            Skills detected from your resume.
          </p>

        </div>

      </div>


      <section className="skills-grid">

        {Object.entries(
          analysis?.skills || {}
        ).map(
          ([category, skills]) => (

            <SkillCard
              key={category}
              category={category}
              skills={skills}
            />

          )
        )}

      </section>

    </div>
  );
}

export default ResumeAnalysis;