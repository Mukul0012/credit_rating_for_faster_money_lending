import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getApplicationForReview, submitDecision } from "../services/lender";
import { getLenderUser, lenderLogout } from "../services/lenderAuth";
import "../styles/lender-review.css";
import "../styles/lender-dashboard.css";

export default function LenderReview() {
  const { applicationId } = useParams();
  const navigate = useNavigate();
  const lenderUser = getLenderUser();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [decisionLoading, setDecisionLoading] = useState(false);
  const [decisionSuccess, setDecisionSuccess] = useState("");
  const [showRejectPanel, setShowRejectPanel] = useState(false);
  const [rejectionReason, setRejectionReason] = useState("");

  const rejectionPresets = [
    "High Debt-to-Income (DTI) ratio exceeding threshold",
    "Credit score below institutional lending policy",
    "History of past payment defaults or excessive delinquencies",
    "Insufficient employment history / stability",
    "Loan amount to income ratio too high",
    "Excessive recent credit inquiries on bureau profile",
  ];

  async function loadApplication() {
    try {
      setLoading(true);
      setError("");
      const res = await getApplicationForReview(applicationId);
      setData(res);
    } catch (err) {
      console.error("Error loading application for review:", err);
      setError(err.message || "Failed to load application details");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadApplication();
  }, [applicationId]);

  async function handleDecision(decisionType, reason = null) {
    try {
      setDecisionLoading(true);
      setError("");
      const result = await submitDecision(applicationId, decisionType, reason);
      setDecisionSuccess(result.message || `Application #${applicationId} marked as ${result.status}`);
      setShowRejectPanel(false);
      // Reload fresh state
      await loadApplication();
    } catch (err) {
      setError(err.message || "Failed to submit decision");
    } finally {
      setDecisionLoading(false);
    }
  }

  function handleLogout() {
    lenderLogout();
    navigate("/lender/login", { replace: true });
  }

  if (loading) {
    return (
      <div className="lender-review-page">
        <div className="lender-review-container" style={{ textAlign: "center", paddingTop: "100px" }}>
          <div className="lender-empty-icon">⏳</div>
          <h2>Loading Applicant Assessment...</h2>
          <p style={{ color: "#94a3b8" }}>Gathering financial records, bureau telemetry, and ML scorecards</p>
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="lender-review-page">
        <div className="lender-review-container" style={{ textAlign: "center", paddingTop: "100px" }}>
          <div className="lender-error" style={{ maxWidth: "500px", margin: "0 auto 20px" }}>
            <span>!</span>
            <div>{error}</div>
          </div>
          <button className="lender-back-btn" onClick={() => navigate("/lender/dashboard")} style={{ margin: "0 auto" }}>
            ← Back to Application Queue
          </button>
        </div>
      </div>
    );
  }

  const { personal, employment, application, credit_profile, credit_rating, loan_request, debt_payment_metrics, existing_loans, assessment } = data || {};

  // Calculations for Gauge Chart (Credit Score: 300 to 850)
  const creditScore = credit_rating?.credit_score || 650;
  const normalizedScore = Math.max(0, Math.min(1, (creditScore - 300) / (850 - 300)));
  const needleRotation = -90 + normalizedScore * 180; // -90deg (300) to +90deg (850)

  let scoreTier = "Good";
  let scoreClass = "good";
  if (creditScore >= 750) {
    scoreTier = "Excellent";
    scoreClass = "excellent";
  } else if (creditScore >= 650) {
    scoreTier = "Good";
    scoreClass = "good";
  } else if (creditScore >= 580) {
    scoreTier = "Fair";
    scoreClass = "fair";
  } else {
    scoreTier = "Poor";
    scoreClass = "poor";
  }

  // Risk Score & Tier
  const riskScoreVal = assessment?.risk_score != null ? Number(assessment.risk_score) : 50;
  const riskColor = riskScoreVal <= 30 ? "#34d399" : riskScoreVal <= 60 ? "#fbbf24" : "#f87171";
  const riskGradClass = riskScoreVal <= 30 ? "low" : riskScoreVal <= 60 ? "medium" : "high";

  // DTI & Utilization
  const dtiVal = credit_profile?.debt_to_income_ratio != null ? Math.round(Number(credit_profile.debt_to_income_ratio) * 100) : 25;
  const utilVal = credit_profile?.credit_utilization != null ? Math.round(Number(credit_profile.credit_utilization) * 100) : 30;

  const dtiCircumference = 2 * Math.PI * 38;
  const dtiOffset = dtiCircumference - (Math.min(dtiVal, 100) / 100) * dtiCircumference;

  const utilCircumference = 2 * Math.PI * 38;
  const utilOffset = utilCircumference - (Math.min(utilVal, 100) / 100) * utilCircumference;

  return (
    <div className="lender-review-page">
      {/* NAVBAR */}
      <nav className="lender-navbar">
        <div className="lender-nav-brand" onClick={() => navigate("/lender/dashboard")}>
          <div className="lender-nav-logo">LP</div>
          <div className="lender-nav-title">
            <strong>CreditFlow</strong>
            <span>Lender Portal</span>
          </div>
        </div>

        <div className="lender-nav-right">
          <div className="lender-user-badge">
            <div className="lender-user-avatar">
              {lenderUser?.full_name ? lenderUser.full_name[0].toUpperCase() : "L"}
            </div>
            <span className="lender-user-name">
              {lenderUser?.full_name || "Lender Underwriter"}
            </span>
          </div>

          <button className="lender-logout-btn" onClick={handleLogout}>
            Sign Out
          </button>
        </div>
      </nav>

      <div className="lender-review-container">
        {/* TOP BAR */}
        <div className="lender-review-top-bar">
          <button className="lender-back-btn" onClick={() => navigate("/lender/dashboard")}>
            ← Back to Application Queue
          </button>

          <span
            className={`lender-status-pill ${
              application?.status?.toLowerCase().replace(/\s+/g, "-") || "pending"
            }`}
            style={{ fontSize: "13px", padding: "6px 16px" }}
          >
            Status: {application?.status || "Pending"}
          </span>
        </div>

        {/* APPLICANT HEADER */}
        <div className="lender-applicant-header">
          <div className="applicant-identity">
            <div className="applicant-avatar">
              {personal?.full_name ? personal.full_name[0].toUpperCase() : "A"}
            </div>
            <div className="applicant-meta">
              <h1>{personal?.full_name}</h1>
              <div className="applicant-tags">
                <span>Application #{application?.application_id}</span>
                <span>•</span>
                <span>Applicant ID: #{personal?.applicant_id}</span>
                <span>•</span>
                <span>Applied: {application?.application_date || "Today"}</span>
              </div>
            </div>
          </div>

          <div className="loan-quick-summary">
            <div className="summary-pill">
              <span>Requested Amount</span>
              <strong>₹{Number(application?.loan_amount || 0).toLocaleString("en-IN")}</strong>
            </div>

            <div className="summary-pill">
              <span>Tenure</span>
              <strong>{application?.loan_tenure || 12} Months</strong>
            </div>

            <div className="summary-pill">
              <span>Purpose</span>
              <strong>{application?.loan_purpose || "Personal"}</strong>
            </div>
          </div>
        </div>

        {/* DECISION FEEDBACK ALERT */}
        {decisionSuccess && (
          <div className="lender-success" style={{ marginBottom: "24px", fontSize: "14px", padding: "14px 20px" }}>
            <span>✓</span>
            <div>{decisionSuccess}</div>
          </div>
        )}

        {/* VISUALIZATION GRID (GAUGE, METERS, DONUT) */}
        <div className="visual-grid">
          {/* 1. CREDIT SCORE GAUGE */}
          <div className="visual-card">
            <div className="visual-card-title">
              <h3>Bureau Credit Score</h3>
              <span className="card-tag">BUREAU ENGINE</span>
            </div>

            <div className="gauge-wrapper">
              <svg className="gauge-svg" viewBox="0 0 220 120">
                <path
                  d="M 20 110 A 90 90 0 0 1 200 110"
                  className="gauge-bg"
                />
                <path
                  d="M 20 110 A 90 90 0 0 1 200 110"
                  className={`gauge-fill ${scoreClass}`}
                  strokeDasharray="282.7"
                  strokeDashoffset={282.7 * (1 - normalizedScore)}
                />
                <line
                  x1="110"
                  y1="110"
                  x2="110"
                  y2="30"
                  stroke="#ffffff"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  className="gauge-needle"
                  style={{ transform: `rotate(${needleRotation}deg)` }}
                />
                <circle cx="110" cy="110" r="7" fill="#6366f1" />
              </svg>

              <div className="gauge-center-text">
                <div className="gauge-score-value">{creditScore}</div>
                <span className={`gauge-rating-badge grade-${(credit_rating?.risk_grade || "c").toLowerCase()}`}>
                  {scoreTier} · Grade {credit_rating?.risk_grade || "C"}
                </span>
              </div>

              <div className="gauge-scale-labels">
                <span>300 (Poor)</span>
                <span>580</span>
                <span>650</span>
                <span>850 (Exceptional)</span>
              </div>
            </div>
          </div>

          {/* 2. ML RISK SCORE & ASSESSMENT */}
          <div className="visual-card">
            <div className="visual-card-title">
              <h3>AI Risk Score</h3>
              <span className="card-tag">RANDOM FOREST ML</span>
            </div>

            <div className="meters-container">
              <div className="meter-block">
                <div className="meter-header">
                  <span>Calculated Risk Assessment</span>
                  <strong style={{ color: riskColor, fontSize: "16px" }}>{riskScoreVal.toFixed(1)} / 100</strong>
                </div>
                <div className="meter-track" style={{ height: "14px" }}>
                  <div
                    className={`meter-fill risk ${riskGradClass}`}
                    style={{ width: `${Math.max(0, Math.min(100, riskScoreVal))}%` }}
                  />
                </div>
                <div className="gauge-scale-labels" style={{ marginTop: "4px" }}>
                  <span>0 (Low Risk)</span>
                  <span>30</span>
                  <span>60</span>
                  <span>100 (Critical)</span>
                </div>
              </div>

              <div style={{ marginTop: "8px", padding: "12px", background: "rgba(15, 23, 42, 0.6)", borderRadius: "8px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: "12px", color: "#94a3b8" }}>ML Suggested Action:</span>
                <span className={`lender-risk-badge ${(assessment?.risk_level || "low").toLowerCase()}`}>
                  {assessment?.decision || "REVIEW"} ({assessment?.risk_level || "MEDIUM"} RISK)
                </span>
              </div>
            </div>
          </div>

          {/* 3. DTI & UTILIZATION RATIOS */}
          <div className="visual-card">
            <div className="visual-card-title">
              <h3>Financial Exposure Ratios</h3>
              <span className="card-tag">CAPACITY</span>
            </div>

            <div className="donut-chart-row">
              {/* DTI DONUT */}
              <div className="donut-item">
                <div className="donut-svg-box">
                  <svg className="donut-svg" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="38" className="donut-bg" />
                    <circle
                      cx="50"
                      cy="50"
                      r="38"
                      className={`donut-stroke ${dtiVal <= 36 ? "good" : dtiVal <= 50 ? "warning" : "danger"}`}
                      strokeDasharray={dtiCircumference}
                      strokeDashoffset={dtiOffset}
                    />
                  </svg>
                  <div className="donut-center-label">{dtiVal}%</div>
                </div>
                <span className="donut-title">Debt-to-Income</span>
              </div>

              {/* UTILIZATION DONUT */}
              <div className="donut-item">
                <div className="donut-svg-box">
                  <svg className="donut-svg" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="38" className="donut-bg" />
                    <circle
                      cx="50"
                      cy="50"
                      r="38"
                      className={`donut-stroke ${utilVal <= 30 ? "good" : utilVal <= 60 ? "warning" : "danger"}`}
                      strokeDasharray={utilCircumference}
                      strokeDashoffset={utilOffset}
                    />
                  </svg>
                  <div className="donut-center-label">{utilVal}%</div>
                </div>
                <span className="donut-title">Credit Utilization</span>
              </div>
            </div>

            <p style={{ fontSize: "11px", color: "#64748b", margin: "6px 0 0", textAlign: "center" }}>
              Standard threshold: DTI ≤ 36%, Utilization ≤ 30%
            </p>
          </div>
        </div>

        {/* TWO COLUMN DETAILS: APPLICANT PROFILE & RISK FACTORS */}
        <div className="review-two-column">
          {/* APPLICANT FINANCIAL & EMPLOYMENT PROFILE */}
          <div className="review-details-card">
            <h3>Applicant Financial & Credit Profile</h3>

            <div className="details-table-grid">
              <div className="detail-cell">
                <span>Annual Income</span>
                <strong>
                  {employment?.annual_income != null
                    ? `₹${Number(employment.annual_income).toLocaleString("en-IN")}`
                    : "N/A"}
                </strong>
              </div>

              <div className="detail-cell">
                <span>Employer & Role</span>
                <strong>{employment?.employer_name || "Self-Employed"} ({employment?.employment_type || "Salaried"})</strong>
              </div>

              <div className="detail-cell">
                <span>Job Tenure</span>
                <strong>{employment?.employment_duration != null ? `${employment.employment_duration} years` : "N/A"}</strong>
              </div>

              <div className="detail-cell">
                <span>Credit History Length</span>
                <strong>{credit_profile?.credit_history_length != null ? `${credit_profile.credit_history_length} yrs` : "N/A"}</strong>
              </div>

              <div className="detail-cell">
                <span>Total Active Accounts</span>
                <strong>{credit_profile?.number_of_credit_accounts ?? "N/A"}</strong>
              </div>

              <div className="detail-cell">
                <span>Total Outstanding Debt</span>
                <strong>
                  {debt_payment_metrics?.total_outstanding_debt != null
                    ? `₹${Number(debt_payment_metrics.total_outstanding_debt).toLocaleString("en-IN")}`
                    : "₹0"}
                </strong>
              </div>

              <div className="detail-cell">
                <span>Existing Monthly EMI</span>
                <strong>
                  {debt_payment_metrics?.monthly_emi != null
                    ? `₹${Number(debt_payment_metrics.monthly_emi).toLocaleString("en-IN")}`
                    : "₹0"}
                </strong>
              </div>

              <div className="detail-cell">
                <span>Loan to Income Ratio</span>
                <strong>
                  {credit_profile?.loan_to_income_ratio != null
                    ? `${(credit_profile.loan_to_income_ratio * 100).toFixed(1)}%`
                    : "N/A"}
                </strong>
              </div>
            </div>
          </div>

          {/* RISK FACTORS & RED FLAGS */}
          <div className="review-details-card">
            <h3>Identified Risk Factors & Bureau Flags</h3>

            {assessment?.risk_factors && assessment.risk_factors.length > 0 ? (
              <div className="risk-factor-badge-list">
                {assessment.risk_factors.map((factor, idx) => (
                  <div key={idx} className="risk-factor-item">
                    <div className="risk-factor-icon">!</div>
                    <span>{factor}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-risk-box">
                <span style={{ fontSize: "18px" }}>✓</span>
                <div>
                  <strong>Clean Credit Record</strong>
                  <div style={{ fontSize: "11px", marginTop: "2px", opacity: 0.85 }}>
                    No significant defaults or high-risk flags identified by the model.
                  </div>
                </div>
              </div>
            )}

            {/* Past Delinquencies / Inquiries Summary */}
            <div style={{ marginTop: "18px", padding: "12px", background: "rgba(15, 23, 42, 0.4)", borderRadius: "8px", fontSize: "12px", color: "#94a3b8" }}>
              <div>• Previous Defaults: <strong style={{ color: credit_profile?.previous_defaults ? "#f87171" : "#34d399" }}>{credit_profile?.previous_defaults ?? 0}</strong></div>
              <div style={{ marginTop: "4px" }}>• Missed Payments: <strong style={{ color: credit_profile?.missed_payments ? "#f87171" : "#34d399" }}>{credit_profile?.missed_payments ?? 0}</strong></div>
              <div style={{ marginTop: "4px" }}>• Recent Bureau Inquiries: <strong style={{ color: credit_profile?.recent_credit_enquiries > 3 ? "#fbbf24" : "#ffffff" }}>{credit_profile?.recent_credit_enquiries ?? 0}</strong></div>
            </div>
          </div>
        </div>

        {/* DECISION ACTION CARD */}
        <div className="decision-action-card">
          <div className="decision-header">
            <div>
              <h2>Underwriter Lending Decision</h2>
              <p style={{ margin: "4px 0 0", fontSize: "13px", color: "#94a3b8" }}>
                Make an official lending determination. Decisions take effect immediately and are communicated to the applicant.
              </p>
            </div>

            {application?.rejection_reason && (
              <span style={{ fontSize: "12px", color: "#f87171", background: "rgba(239, 68, 68, 0.1)", padding: "6px 12px", borderRadius: "6px", border: "1px solid rgba(239, 68, 68, 0.25)" }}>
                Reason on file: {application.rejection_reason}
              </span>
            )}
          </div>

          <div className="decision-buttons-row">
            <button
              className="decide-btn approve"
              onClick={() => handleDecision("APPROVE")}
              disabled={decisionLoading || application?.status === "Approved"}
            >
              <span>✓</span> Approve Application
            </button>

            <button
              className="decide-btn reject"
              onClick={() => setShowRejectPanel(!showRejectPanel)}
              disabled={decisionLoading || application?.status === "Rejected"}
            >
              <span>✕</span> {showRejectPanel ? "Cancel Rejection" : "Reject Application"}
            </button>
          </div>

          {/* REJECTION REASON PANEL */}
          {showRejectPanel && (
            <div className="rejection-panel">
              <label>Select or Enter Rejection Reason (Shown to Applicant):</label>

              <div className="reason-presets">
                {rejectionPresets.map((preset, idx) => (
                  <button
                    key={idx}
                    type="button"
                    className="preset-chip"
                    onClick={() => setRejectionReason(preset)}
                  >
                    + {preset}
                  </button>
                ))}
              </div>

              <textarea
                className="rejection-textarea"
                placeholder="Explain specific reasons for loan rejection..."
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
              />

              <button
                type="button"
                className="confirm-reject-btn"
                onClick={() => handleDecision("REJECT", rejectionReason)}
                disabled={decisionLoading}
              >
                {decisionLoading ? "Processing Rejection..." : "Confirm & Send Rejection Decision"}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
