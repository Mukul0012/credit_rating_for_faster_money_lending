function ApplicationTable({
  applications
}) {

  return (
    <div className="panel">

      <div className="panel-header">

        <div>

          <span className="eyebrow">
            HISTORY
          </span>

          <h2>
            Recent Applications
          </h2>

        </div>

      </div>


      {applications.length === 0 ? (

        <div className="empty-state">
          No applications found.
        </div>

      ) : (

        <div className="table-wrapper">

          <table className="application-table">

            <thead>

              <tr>

                <th>
                  Application
                </th>

                <th>
                  Date
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
                (application) => (

                  <tr
                    key={
                      application.application_id
                    }
                  >

                    <td>
                      <strong>
                        #
                        {
                          application.application_id
                        }
                      </strong>
                    </td>

                    <td>
                      {
                        application.application_date
                      }
                    </td>

                    <td>
                      ₹
                      {Number(
                        application.loan_amount
                      ).toLocaleString(
                        "en-IN"
                      )}
                    </td>

                    <td>
                      {
                        application.loan_purpose
                      }
                    </td>

                    <td>

                      <span className="status-badge pending">
                        {
                          application.status
                        }
                      </span>

                    </td>

                    <td>

                      {application.decision ? (

                        <span
                          className={`decision-badge ${
                            application.decision
                              .toLowerCase()
                          }`}
                        >
                          {
                            application.decision
                          }
                        </span>

                      ) : (

                        <span className="muted">
                          Not assessed
                        </span>

                      )}

                    </td>

                    <td>
                      {
                        application.risk_level
                        || "N/A"
                      }
                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      )}

    </div>
  );
}


export default ApplicationTable;