function RiskAssessment({
  assessment
}) {

  if (!assessment) {

    return (
      <div className="panel">

        <div className="panel-header">

          <div>
            <span className="eyebrow">
              RISK ASSESSMENT
            </span>

            <h2>
              Assessment
            </h2>
          </div>

        </div>

        <div className="empty-state">
          No assessment available.
        </div>

      </div>
    );
  }


  const probability =
    Number(
      assessment.approval_probability
    ) * 100;


  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <span className="eyebrow">
            RISK ASSESSMENT
          </span>

          <h2>
            Current Assessment
          </h2>
        </div>

        <span
          className={`decision-badge ${
            assessment.decision
              ?.toLowerCase()
          }`}
        >
          {assessment.decision}
        </span>

      </div>


      <div className="risk-grid">

        <div className="risk-metric">

          <span>
            Approval Probability
          </span>

          <strong>
            {probability.toFixed(1)}%
          </strong>

          <div className="progress-bar">

            <div
              className="progress-fill"
              style={{
                width: `${probability}%`
              }}
            />

          </div>

        </div>


        <div className="risk-metric">

          <span>
            Risk Score
          </span>

          <strong>
            {assessment.risk_score}
          </strong>

        </div>


        <div className="risk-metric">

          <span>
            Risk Level
          </span>

          <strong>
            {assessment.risk_level}
          </strong>

        </div>

      </div>


      <div className="risk-factors">

        <h3>
          Key Risk Factors
        </h3>

        {assessment.risk_factors?.length ? (

          <div className="factor-list">

            {assessment.risk_factors.map(
              (factor, index) => (

                <div
                  className="factor"
                  key={index}
                >
                  <span className="factor-dot">
                    !
                  </span>

                  {factor}

                </div>

              )
            )}

          </div>

        ) : (

          <p className="muted">
            No significant risk
            factors identified.
          </p>

        )}

      </div>

    </div>
  );
}


export default RiskAssessment;