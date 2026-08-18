import {
  useEffect,
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import {
  getMyProfile
} from "../services/applicant";

import "../styles/credit-profile.css";


function CreditProfile() {

  const navigate = useNavigate();

  const [profile, setProfile] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  // =========================================
  // FETCH PROFILE
  // =========================================

  useEffect(() => {

    async function loadProfile() {

      try {

        setLoading(true);
        setError("");

        const data =
          await getMyProfile();

        setProfile(data);

      } catch (err) {

        console.error(
          "Credit profile error:",
          err
        );

        setError(
          err.message ||
          "Unable to load credit profile."
        );

      } finally {

        setLoading(false);

      }

    }

    loadProfile();

  }, []);


  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (
      <div className="credit-profile-page">

        <div className="credit-profile-loading">

          <div className="loading-spinner" />

          <p>
            Loading credit profile...
          </p>

        </div>

      </div>
    );

  }


  // =========================================
  // ERROR
  // =========================================

  if (error) {

    return (
      <div className="credit-profile-page">

        <div className="credit-profile-error">

          <h2>
            Unable to load credit profile
          </h2>

          <p>
            {error}
          </p>

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


  if (!profile) {
    return null;
  }


  // =========================================
  // DATA
  // =========================================

  const personal =
    profile.personal || {};

  const employment =
    profile.employment || {};

  const creditProfile =
    profile.credit_profile || {};

  const creditRating =
    profile.credit_rating || {};

  const debtMetrics =
    profile.debt_payment_metrics || {};

  const existingLoans =
    Array.isArray(
      profile.existing_loans
    )
      ? profile.existing_loans
      : [];


  const creditScore =
    creditRating.credit_score;

  const riskGrade =
    creditRating.risk_grade;


  return (

    <div className="credit-profile-page">

      <div className="credit-profile-container">


        {/* =================================
            HEADER
        ================================= */}

        <button
          className="credit-profile-back"
          onClick={() =>
            navigate("/dashboard")
          }
        >
          ← Back to Dashboard
        </button>


        <div className="credit-profile-header">

          <div>

            <span className="eyebrow">
              CREDIT INFORMATION
            </span>

            <h1>
              Credit Profile
            </h1>

            <p>
              Complete overview of your
              current credit information.
            </p>

          </div>

        </div>


        {/* =================================
            CREDIT SCORE
        ================================= */}

        <section className="credit-score-section">

          <div className="credit-score-card">

            <span className="score-label">
              CREDIT SCORE
            </span>

            <div className="score-value">
              {creditScore ?? "N/A"}
            </div>

            <span className="score-description">
              Current credit score
            </span>

          </div>


          <div className="risk-grade-card">

            <span className="score-label">
              RISK GRADE
            </span>

            <div
              className={
                `risk-grade ${
                  getRiskGradeClass(
                    riskGrade
                  )
                }`
              }
            >
              {riskGrade || "N/A"}
            </div>

            <span className="score-description">
              Current credit risk grade
            </span>

          </div>

        </section>


        {/* =================================
            CREDIT METRICS
        ================================= */}

        <section className="credit-panel">

          <div className="credit-panel-header">

            <div>

              <span className="eyebrow">
                CREDIT PROFILE
              </span>

              <h2>
                Credit Metrics
              </h2>

            </div>

          </div>


          <div className="credit-metrics-grid">

            <Metric
              label="Credit Utilization"
              value={
                formatPercentage(
                  creditProfile.credit_utilization
                )
              }
            />

            <Metric
              label="Payment History"
              value={
                formatPercentage(
                  creditProfile.payment_history
                )
              }
            />

            <Metric
              label="Debt-to-Income Ratio"
              value={
                formatPercentage(
                  creditProfile.debt_to_income_ratio
                )
              }
            />

            <Metric
              label="Loan-to-Income Ratio"
              value={
                formatPercentage(
                  creditProfile.loan_to_income_ratio
                )
              }
            />

            <Metric
              label="Previous Defaults"
              value={
                creditProfile.previous_defaults ??
                "N/A"
              }
            />

            <Metric
              label="Missed Payments"
              value={
                creditProfile.missed_payments ??
                "N/A"
              }
            />

            <Metric
              label="Maximum Days Past Due"
              value={
                creditProfile.maximum_days_past_due ??
                "N/A"
              }
            />

            <Metric
              label="Recent Credit Enquiries"
              value={
                creditProfile.recent_credit_enquiries ??
                "N/A"
              }
            />

            <Metric
              label="Credit Accounts"
              value={
                creditProfile.number_of_credit_accounts ??
                "N/A"
              }
            />

            <Metric
              label="Credit History"
              value={
                creditProfile.credit_history_length != null
                  ? `${creditProfile.credit_history_length} years`
                  : "N/A"
              }
            />

          </div>

        </section>


        {/* =================================
            DEBT INFORMATION
        ================================= */}

        <section className="credit-panel">

          <div className="credit-panel-header">

            <div>

              <span className="eyebrow">
                DEBT & PAYMENT
              </span>

              <h2>
                Existing Debt
              </h2>

            </div>

          </div>


          <div className="credit-metrics-grid">

            <Metric
              label="Existing Loans"
              value={
                debtMetrics.existing_loans_count ??
                existingLoans.length ??
                "N/A"
              }
            />

            <Metric
              label="Outstanding Debt"
              value={
                formatCurrency(
                  debtMetrics.total_outstanding_debt
                )
              }
            />

            <Metric
              label="Monthly EMI"
              value={
                formatCurrency(
                  debtMetrics.monthly_emi
                )
              }
            />

          </div>


          {/* EXISTING LOANS */}

          {existingLoans.length > 0 && (

            <div className="existing-loans">

              <h3>
                Existing Loans
              </h3>


              <div className="existing-loans-list">

                {existingLoans.map(
                  (loan) => (

                    <div
                      className="existing-loan"
                      key={
                        loan.existing_loan_id
                      }
                    >

                      <div>

                        <strong>
                          {loan.loan_type ||
                            "Loan"}
                        </strong>

                        <span>
                          Loan Amount:{" "}
                          {formatCurrency(
                            loan.loan_amount
                          )}
                        </span>

                      </div>


                      <div>

                        <strong>
                          {formatCurrency(
                            loan.outstanding_amount
                          )}
                        </strong>

                        <span>
                          Outstanding
                        </span>

                      </div>


                      <div>

                        <strong>
                          {formatCurrency(
                            loan.monthly_emi
                          )}
                        </strong>

                        <span>
                          Monthly EMI
                        </span>

                      </div>

                    </div>

                  )
                )}

              </div>

            </div>

          )}

        </section>


        {/* =================================
            EMPLOYMENT
        ================================= */}

        <section className="credit-panel">

          <div className="credit-panel-header">

            <div>

              <span className="eyebrow">
                FINANCIAL PROFILE
              </span>

              <h2>
                Employment
              </h2>

            </div>

          </div>


          <div className="credit-metrics-grid">

            <Metric
              label="Employment Type"
              value={
                employment.employment_type ||
                "N/A"
              }
            />

            <Metric
              label="Employer"
              value={
                employment.employer_name ||
                "N/A"
              }
            />

            <Metric
              label="Annual Income"
              value={
                formatCurrency(
                  employment.annual_income
                )
              }
            />

            <Metric
              label="Employment Duration"
              value={
                employment.employment_duration != null
                  ? `${employment.employment_duration} years`
                  : "N/A"
              }
            />

          </div>

        </section>


        {/* =================================
            FOOTER ACTION
        ================================= */}

        <div className="credit-profile-actions">

          <button
            className="secondary-button"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Back to Dashboard
          </button>

          <button
            className="primary-button"
            onClick={() =>
              navigate("/apply-loan")
            }
          >
            Apply for New Loan
          </button>

        </div>

      </div>

    </div>

  );

}


/* =========================================
   METRIC COMPONENT
========================================= */

function Metric({
  label,
  value
}) {

  return (

    <div className="credit-metric">

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
   FORMAT HELPERS
========================================= */

function formatPercentage(
  value
) {

  if (value == null) {
    return "N/A";
  }

  const number =
    Number(value);

  if (Number.isNaN(number)) {
    return "N/A";
  }

  /*
   * Backend may return either:
   *
   * 0.16  -> 16%
   * 16    -> 16%
   */

  const percentage =
    number <= 1
      ? number * 100
      : number;

  return `${percentage.toFixed(1)}%`;

}


function formatCurrency(
  value
) {

  if (value == null) {
    return "N/A";
  }

  const number =
    Number(value);

  if (Number.isNaN(number)) {
    return "N/A";
  }

  return `₹${number.toLocaleString(
    "en-IN"
  )}`;

}


function getRiskGradeClass(
  grade
) {

  if (!grade) {
    return "";
  }

  return `grade-${grade
    .toLowerCase()
    .replace(/\s+/g, "-")}`;

}


export default CreditProfile;