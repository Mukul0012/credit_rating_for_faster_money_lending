function CreditScoreCard({
  score,
  grade
}) {

  const percentage =
    Math.min(
      Math.max(
        ((score - 300) / 600) * 100,
        0
      ),
      100
    );


  return (
    <div className="credit-score-card">

      <div className="card-heading">

        <div>
          <span className="eyebrow">
            CREDIT PROFILE
          </span>

          <h2>
            Credit Score
          </h2>
        </div>

        <div className="grade-badge">
          Grade {grade || "N/A"}
        </div>

      </div>


      <div className="score-content">

        <div className="score-circle">

          <svg
            viewBox="0 0 120 120"
            className="score-svg"
          >

            <circle
              cx="60"
              cy="60"
              r="50"
              className="score-track"
            />

            <circle
              cx="60"
              cy="60"
              r="50"
              className="score-progress"
              style={{
                strokeDasharray: 314,
                strokeDashoffset:
                  314 -
                  (314 * percentage) /
                  100
              }}
            />

          </svg>

          <div className="score-number">
            {score ?? "—"}
          </div>

        </div>


        <div className="score-info">

          <div className="score-label">
            Credit health
          </div>

          <div className="score-status">
            {score >= 750
              ? "Excellent"
              : score >= 700
                ? "Good"
                : score >= 650
                  ? "Fair"
                  : "Needs attention"}
          </div>

          <p>
            Your score is based on your
            credit history, payment
            behaviour and outstanding
            obligations.
          </p>

        </div>

      </div>

    </div>
  );
}


export default CreditScoreCard;