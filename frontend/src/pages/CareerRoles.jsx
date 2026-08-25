import RoleCard from "../components/RoleCard";

function CareerRoles({
  analysis
}) {

  return (
    <div>

      <div className="dashboard-header">

        <div>

          <span className="eyebrow">
            CAREER RECOMMENDATIONS
          </span>

          <h2>
            Roles You Could Target
          </h2>

          <p>
            Ranked using your skills,
            projects, and experience.
          </p>

        </div>

      </div>


      <div className="roles-grid">

        {analysis
          ?.suggested_roles
          ?.map(
            (role, index) => (

              <RoleCard
                key={role.role}
                role={role}
                rank={index + 1}
              />

            )
          )}

      </div>

    </div>
  );
}

export default CareerRoles;