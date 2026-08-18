import { useNavigate } from "react-router-dom";

import "../styles/dashboard.css";


function ApplicationTable({
  applications = []
}) {

  const navigate =
    useNavigate();


  if (!applications.length) {

    return (
      <div className="applications-empty">

        <div className="empty-icon">
          📄
        </div>

        <h3>
          No loan applications
        </h3>

        <p>
          You have not submitted any
          loan applications yet.
        </p>

        <button
          className="primary-button"
          onClick={() =>
            navigate("/apply-loan")
          }
        >
          Apply for New Loan
        </button>

      </div>
    );

  }


  return (

    <div className="applications-table-wrapper">

      <table className="applications-table">

        <thead>

          <tr>

            <th>
              Application
            </th>

            <th>
              Amount
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

          </tr>

        </thead>


        <tbody>

          {applications.map(
            (application) => {

              const hasAssessment =
                application.assessment_id !==
                null;


              return (

                <tr
                  key={
                    application.application_id
                  }
                >

                  {/* APPLICATION */}

                  <td>

                    <button
                      className="application-link"
                      onClick={() =>
                        navigate(
                          `/application/${application.application_id}`
                        )
                      }
                    >
                      #
                      {
                        application.application_id
                      }
                    </button>

                  </td>


                  {/* AMOUNT */}

                  <td>

                    ₹
                    {Number(
                      application.loan_amount || 0
                    ).toLocaleString(
                      "en-IN"
                    )}

                  </td>


                  {/* PURPOSE */}

                  <td>

                    {application.loan_purpose ||
                      "N/A"}

                  </td>


                  {/* STATUS */}

                  <td>

                    <span
                      className={
                        `table-status ${
                          (
                            application.status ||
                            ""
                          ).toLowerCase()
                        }`
                      }
                    >
                      {
                        application.status ||
                        "N/A"
                      }
                    </span>

                  </td>


                  {/* DECISION */}

                  <td>

                    {hasAssessment ? (

                      <span
                        className={
                          `decision-badge-small ${
                            (
                              application.decision ||
                              ""
                            ).toLowerCase()
                          }`
                        }
                      >
                        {
                          application.decision ||
                          "N/A"
                        }
                      </span>

                    ) : (

                      <span className="not-assessed">
                        Not assessed
                      </span>

                    )}

                  </td>


                  {/* RISK */}

                  <td>

                    {hasAssessment ? (

                      <span
                        className={
                          `risk-badge ${
                            (
                              application.risk_level ||
                              ""
                            ).toLowerCase()
                          }`
                        }
                      >
                        {
                          application.risk_level ||
                          "N/A"
                        }
                      </span>

                    ) : (

                      <span className="risk-na">
                        N/A
                      </span>

                    )}

                  </td>

                </tr>

              );

            }
          )}

        </tbody>

      </table>

    </div>

  );

}


export default ApplicationTable;