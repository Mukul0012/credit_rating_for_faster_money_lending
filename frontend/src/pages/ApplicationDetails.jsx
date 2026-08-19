import {
  useEffect,
  useState
} from "react";

import {
  useNavigate,
  useParams
} from "react-router-dom";

import {
  getApplicationDetails
} from "../services/loan";

import "../styles/application-details.css";


function ApplicationDetails() {

  const {
    applicationId
  } = useParams();

  const navigate =
    useNavigate();


  const [data, setData] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  // =========================================
  // FETCH APPLICATION FROM BACKEND
  // =========================================

  useEffect(() => {

    async function loadApplication() {

      if (!applicationId) {

        setError(
          "Application ID is missing."
        );

        setLoading(false);

        return;
      }


      try {

        setLoading(true);

        setError("");

        /*
         * IMPORTANT:
         *
         * We intentionally fetch the application
         * from the backend instead of using
         * React Router state.
         *
         * This makes the page work when:
         *
         * - user refreshes the page
         * - user opens /application/106 directly
         * - user comes from Loan History
         * - user comes from Dashboard
         *
         * PostgreSQL/API is the source of truth.
         */

        const response =
          await getApplicationDetails(
            applicationId
          );


        if (!response) {

          throw new Error(
            "Application not found."
          );

        }


        setData(response);

      } catch (err) {

        console.error(
          "Application details error:",
          err
        );


        setError(
          err.message ||
          "Unable to load application."
        );

      } finally {

        setLoading(false);

      }

    }


    loadApplication();

  }, [applicationId]);


  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (

      <div className="application-loading">

        <div className="loading-spinner" />

        <p>
          Loading application...
        </p>

      </div>

    );

  }


  // =========================================
  // ERROR
  // =========================================

  if (error) {

    return (

      <div className="application-error">

        <h2>
          Unable to load application
        </h2>

        <p>
          {error}
        </p>


        <div className="application-error-actions">

          <button
            onClick={() =>
              navigate("/loan-history")
            }
          >
            View Applications
          </button>


          <button
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Back to Dashboard
          </button>

        </div>

      </div>

    );

  }


  // =========================================
  // NO DATA
  // =========================================

  if (!data) {

    return (

      <div className="application-error">

        <h2>
          Application not found
        </h2>

        <p>
          We could not find this loan application.
        </p>


        <button
          onClick={() =>
            navigate("/loan-history")
          }
        >
          View Applications
        </button>

      </div>

    );

  }


  const application =
    data.application;


  const assessment =
    data.assessment;


  // =========================================
  // APPROVAL PROBABILITY
  // =========================================

  const probability =
    assessment?.approval_probability != null
      ? Number(
          assessment.approval_probability
        ) * 100
      : null;


  // =========================================
  // RISK SCORE
  // =========================================

  const riskScore =
    assessment?.risk_score != null
      ? Number(
          assessment.risk_score
        )
      : null;


  // =========================================
  // RISK LEVEL
  // =========================================

  const riskLevel =
    assessment?.risk_level ||
    null;


  // =========================================
  // DECISION
  // =========================================

  const decision =
    assessment?.decision ||
    null;


  // =========================================
  // RISK FACTORS
  // =========================================

  const riskFactors =
    Array.isArray(
      assessment?.risk_factors
    )
      ? assessment.risk_factors
      : [];


  return (

    <div className="application-page">

      <div className="application-container">


        {/* =================================
            BACK BUTTON
        ================================= */}

        <button
          className="application-back"
          onClick={() =>
            navigate("/dashboard")
          }
        >
          ← Back to Dashboard
        </button>


        {/* =================================
            HEADER
        ================================= */}

        <div className="application-header">

          <div>

            <span className="eyebrow">
              LOAN APPLICATION
            </span>


            <h1>
              Application #
              {application.application_id}
            </h1>


            <p>
              Submitted on{" "}
              {application.application_date}
            </p>

          </div>


          <span
            className={
              `status-badge ${
                application.status
                  ?.toLowerCase()
                  .replace(/\s+/g, "-")
              }`
            }
          >
            {application.status}
          </span>

        </div>


        {/* =================================
            STATUS BANNERS
        ================================= */}

        {application.status === "Rejected" && (
          <div className="rejection-banner">
            <div className="rejection-banner-header">
              <div className="rejection-banner-icon">✕</div>
              <div className="rejection-banner-title">Application Declined</div>
            </div>
            <p className="rejection-banner-reason">
              <strong>Reason: </strong>
              {application.rejection_reason || "Your application did not meet the required credit risk criteria."}
            </p>
            <p className="rejection-banner-tip">
              Tip: You may improve your approval odds by reducing existing outstanding debt, maintaining on-time EMI repayments, or applying for a lower loan amount.
            </p>
          </div>
        )}

        {(application.status === "Pending" || application.status === "Under Review") && (
          <div className="pending-review-banner">
            <div className="pending-review-header">
              <div className="pending-review-icon">⌛</div>
              <div className="pending-review-title">Under Review by Lender</div>
            </div>
            <p className="pending-review-desc">
              Your application has been received and is currently in the underwriter queue for evaluation. You will be notified as soon as a lending decision has been finalized.
            </p>
          </div>
        )}


        {/* =================================
            LOAN DETAILS
        ================================= */}

        <section className="details-panel">

          <div className="details-panel-header">

            <div>

              <span className="eyebrow">
                APPLICATION
              </span>


              <h2>
                Loan Details
              </h2>

            </div>

          </div>


          <div className="details-grid">

            <Detail
              label="Loan Amount"
              value={
                application.loan_amount != null
                  ? `₹${Number(
                      application.loan_amount
                    ).toLocaleString("en-IN")}`
                  : "N/A"
              }
            />


            <Detail
              label="Loan Tenure"
              value={
                application.loan_tenure != null
                  ? `${application.loan_tenure} months`
                  : "N/A"
              }
            />


            <Detail
              label="Loan Purpose"
              value={
                application.loan_purpose ||
                "N/A"
              }
            />


            <Detail
              label="Application Status"
              value={
                application.status ||
                "N/A"
              }
            />

          </div>

        </section>


        {/* =================================
            CREDIT RISK ASSESSMENT
        ================================= */}

        <section className="details-panel">

          <div className="details-panel-header">

            <div>

              <span className="eyebrow">
                CREDIT RISK ENGINE
              </span>


              <h2>
                Risk Assessment
              </h2>

            </div>


            {decision && (

              <span
                className={
                  `decision-badge ${
                    decision.toLowerCase()
                  }`
                }
              >
                {decision}
              </span>

            )}

          </div>


          {/* =================================
              NOT ASSESSED
          ================================= */}

          {!assessment ? (

            <div className="not-assessed">

              <div className="not-assessed-icon">
                —
              </div>


              <h3>
                This application has not
                been assessed yet.
              </h3>


              <p>
                Credit risk assessment
                results will appear here
                once the application is
                processed.
              </p>

            </div>

          ) : (

            <>

              {/* =============================
                  METRICS
              ============================== */}

              <div className="assessment-grid">

                <AssessmentMetric
                  label="Prediction"
                  value={
                    assessment.prediction ??
                    "N/A"
                  }
                />


                <AssessmentMetric
                  label="Approval Probability"
                  value={
                    probability !== null
                      ? `${probability.toFixed(1)}%`
                      : "N/A"
                  }
                />


                <AssessmentMetric
                  label="Risk Score"
                  value={
                    riskScore !== null
                      ? riskScore.toFixed(2)
                      : "N/A"
                  }
                />


                <AssessmentMetric
                  label="Risk Level"
                  value={
                    riskLevel ||
                    "N/A"
                  }
                />

              </div>


              {/* =============================
                  APPROVAL PROBABILITY
              ============================== */}

              {probability !== null && (

                <div className="probability-section">

                  <div className="probability-header">

                    <span>
                      Approval Probability
                    </span>


                    <strong>
                      {probability.toFixed(1)}%
                    </strong>

                  </div>


                  <div className="probability-track">

                    <div
                      className="probability-fill"
                      style={{
                        width:
                          `${Math.max(
                            0,
                            Math.min(
                              probability,
                              100
                            )
                          )}%`
                      }}
                    />

                  </div>

                </div>

              )}


              {/* =============================
                  RISK FACTORS
              ============================== */}

              <div className="factors-section">

                <h3>
                  Risk Factors
                </h3>


                {riskFactors.length > 0 ? (

                  <div className="application-factors">

                    {riskFactors.map(
                      (
                        factor,
                        index
                      ) => (

                        <div
                          className="application-factor"
                          key={`${factor}-${index}`}
                        >

                          <span>
                            !
                          </span>

                          {factor}

                        </div>

                      )
                    )}

                  </div>

                ) : (

                  <p className="no-factors">
                    No significant risk
                    factors identified.
                  </p>

                )}

              </div>

            </>

          )}

        </section>


        {/* =================================
            ACTIONS
        ================================= */}

        <div className="application-actions">

          <button
            className="secondary-button"
            onClick={() =>
              navigate("/loan-history")
            }
          >
            View All Applications
          </button>


          <button
            className="secondary-button"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Back to Dashboard
          </button>

        </div>

      </div>

    </div>

  );

}


/* =========================================
   DETAIL COMPONENT
========================================= */

function Detail({
  label,
  value
}) {

  return (

    <div className="detail-box">

      <span>
        {label}
      </span>


      <strong>
        {value ?? "N/A"}
      </strong>

    </div>

  );

}


/* =========================================
   ASSESSMENT METRIC
========================================= */

function AssessmentMetric({
  label,
  value
}) {

  return (

    <div className="assessment-metric">

      <span>
        {label}
      </span>


      <strong>
        {value ?? "N/A"}
      </strong>

    </div>

  );

}


export default ApplicationDetails;