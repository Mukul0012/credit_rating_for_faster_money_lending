export default function RiskBadge({
  level
}) {

  if (!level) {
    return (
      <span className="badge">
        Pending
      </span>
    );
  }

  return (
    <span
      className={`badge ${level.toLowerCase()}`}
    >
      {level}
    </span>
  );
}