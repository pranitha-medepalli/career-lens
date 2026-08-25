function SkillCard({ category, skills }) {
  return (
    <div className="skill-card">
      <h3>{category}</h3>

      <div className="tag-container">
        {skills.map((skill) => (
          <span
            className="tag"
            key={`${category}-${skill}`}
          >
            {skill}
          </span>
        ))}
      </div>
    </div>
  );
}

export default SkillCard;