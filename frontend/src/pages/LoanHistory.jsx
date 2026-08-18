import {
  useEffect,
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import {
  getLoanHistory
} from "../services/loan";

import "../styles/loan-history.css";


function LoanHistory() {

  const navigate =
    useNavigate();

  const [applications, setApplications] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  // =========================================
  // LOAD LOAN HISTORY
  // =========================================

  useEffect(() => {

    async function loadHistory() {

      try {

        setLoading(true);

        setError("");

        const response =
          await getLoanHistory();

        setApplications(
          response?.applications || []
        );

      } catch (err) {

        console.error(
          "Loan history error:",
          err
        );

        setError(
          err.message ||
          "Unable to load loan history."
        );

      } finally {

        setLoading(false);

      }

    }


    loadHistory();

  }, []);


  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (

      <div className="loan-history-page">

        <div className="loan-history-loading">

          <div className="loading-spinner" />

          <p>
            Loading loan applications...
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

      <div className="loan-history-page">

        <div className="loan-history-error">

          <h2>
            Unable to load applications
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


  // =========================================
  // OPEN APPLICATION
  // =========================================

  function openApplication(
    applicationId
  ) {

    navigate(
      `/application/${applicationId}`
    );

  }


  // =========================================
  // PAGE
  // =========================================

  return (

    <div className="loan-history-page">

      <div className="loan-history-container">


        {/* =================================
            HEADER
        ================================= */}

        <div className="loan-history-header">

          <div>

            <button
              className="loan-history-back"
              onClick={() =>
                navigate("/dashboard")
              }
            >
              ← Back to Dashboard
            </button>


            <span className="eyebrow">
              CREDIT APPLICATIONS
            </span>


            <h1>
              Loan History
            </h1>


            <p>
              View all your previous and
              current loan applications.
            </p>

          </div>


          <button
            className="new-loan-button"
            onClick={() =>
              navigate("/apply-loan")
            }
          >
            + Apply for New Loan
          </button>

        </div>


        {/* =================================
            SUMMARY
        ================================= */}

        <div className="loan-history-summary">

          <div className="summary-card">

            <span>
              Total Applications
            </span>

            <strong>
              {applications.length}
            </strong>

          </div>


          <div className="summary-card">

            <span>
              Under Review
            </span>

            <strong>
              {
                applications.filter(
                  (application) =>
                    normalizeStatus(
                      application.status
                    ) === "under-review"
                ).length
              }
            </strong>

          </div>


          <div className="summary-card">

            <span>
              Approved
            </span>

            <strong>
              {
                applications.filter(
                  (application) =>
                    normalizeStatus(
                      application.status
                    ) === "approved"
                ).length
              }
            </strong>

          </div>


          <div className="summary-card">

            <span>
              Rejected
            </span>

            <strong>
              {
                applications.filter(
                  (application) =>
                    normalizeStatus(
                      application.status
                    ) === "rejected"
                ).length
              }
            </strong>

          </div>

        </div>


        {/* =================================
            EMPTY STATE
        ================================= */}

        {applications.length === 0 ? (

          <div className="loan-history-empty">

            <div className="empty-icon">
              +
            </div>


            <h2>
              No loan applications yet
            </h2>


            <p>
              You haven't submitted any
              loan applications.
            </p>


            <button
              onClick={() =>
                navigate("/apply-loan")
              }
            >
              Apply for Your First Loan
            </button>

          </div>

        ) : (

          /* =================================
             APPLICATION TABLE
          ================================= */

          <section className="loan-history-panel">

            <div className="loan-history-panel-header">

              <div>

                <span className="eyebrow">
                  APPLICATIONS
                </span>

                <h2>
                  All Applications
                </h2>

              </div>

            </div>


            <div className="loan-table-wrapper">

              <table className="loan-table">

                <thead>

                  <tr>

                    <th>
                      Application
                    </th>

                    <th>
                      Date
                    </th>

                    <th>
                      Loan Amount
                    </th>

                    <th>
                      Purpose
                    </th>

                    <th>
                      Status
                    </th>

                    <th>
                      Decision
                    </th>

                    <th>
                      Risk
                    </th>

                    <th>
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {applications.map(
                    (application) => (

                      <tr
                        key={
                          application.application_id
                        }
                        className="loan-row"
                        onClick={() =>
                          openApplication(
                            application.application_id
                          )
                        }
                      >

                        {/* APPLICATION */}

                        <td>

                          <strong>
                            #
                            {
                              application.application_id
                            }
                          </strong>

                        </td>


                        {/* DATE */}

                        <td>

                          {formatDate(
                            application.application_date
                          )}

                        </td>


                        {/* AMOUNT */}

                        <td>

                          <strong>

                            ₹
                            {Number(
                              application.loan_amount || 0
                            ).toLocaleString(
                              "en-IN"
                            )}

                          </strong>

                        </td>


                        {/* PURPOSE */}

                        <td>

                          {application.loan_purpose ||
                            "N/A"}

                        </td>


                        {/* STATUS */}

                        <td>

                          <StatusBadge
                            status={
                              application.status
                            }
                          />

                        </td>


                        {/* DECISION */}

                        <td>

                          {application.decision ? (

                            <DecisionBadge
                              decision={
                                application.decision
                              }
                            />

                          ) : (

                            <span className="muted-value">
                              Not assessed
                            </span>

                          )}

                        </td>


                        {/* RISK */}

                        <td>

                          {application.risk_level ? (

                            <RiskBadge
                              risk={
                                application.risk_level
                              }
                            />

                          ) : (

                            <span className="muted-value">
                              N/A
                            </span>

                          )}

                        </td>


                        {/* OPEN */}

                        <td>

                          <span className="open-application">
                            →
                          </span>

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          </section>

        )}

      </div>

    </div>

  );

}


/* =========================================
   STATUS BADGE
========================================= */

function StatusBadge({
  status
}) {

  const normalized =
    normalizeStatus(status);


  return (

    <span
      className={
        `history-status ${normalized}`
      }
    >
      {status || "N/A"}
    </span>

  );

}


/* =========================================
   DECISION BADGE
========================================= */

function DecisionBadge({
  decision
}) {

  const normalized =
    decision
      ?.toLowerCase();


  return (

    <span
      className={
        `history-decision ${normalized}`
      }
    >
      {decision}
    </span>

  );

}


/* =========================================
   RISK BADGE
========================================= */

function RiskBadge({
  risk
}) {

  const normalized =
    risk
      ?.toLowerCase();


  return (

    <span
      className={
        `history-risk ${normalized}`
      }
    >
      {risk}
    </span>

  );

}


/* =========================================
   HELPERS
========================================= */

function normalizeStatus(
  status
) {

  return (
    status
      ?.toLowerCase()
      .replace(/\s+/g, "-") ||
    "unknown"
  );

}


function formatDate(
  date
) {

  if (!date) {
    return "N/A";
  }


  const parsed =
    new Date(date);


  if (Number.isNaN(
    parsed.getTime()
  )) {

    return date;

  }


  return parsed.toLocaleDateString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric"
    }
  );

}


export default LoanHistory;