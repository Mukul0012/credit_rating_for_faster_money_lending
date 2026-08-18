function LatestApplication({
  application
}) {

  if (!application) {

    return (
      <div className="panel">

        <div className="panel-header">
          <div>
            <span className="eyebrow">
              LOAN
            </span>

            <h2>
              Latest Application
            </h2>
          </div>
        </div>

        <div className="empty-state">
          No loan application found.
        </div>

      </div>
    );
  }


  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <span className="eyebrow">
            LATEST APPLICATION
          </span>

          <h2>
            Application #{application.application_id}
          </h2>
        </div>

        <span className="status-badge pending">
          {application.status}
        </span>

      </div>


      <div className="application-details">

        <div className="detail-item">

          <span>
            Loan Amount
          </span>

          <strong>
            ₹
            {Number(
              application.loan_amount
            ).toLocaleString("en-IN")}
          </strong>

        </div>


        <div className="detail-item">

          <span>
            Tenure
          </span>

          <strong>
            {application.loan_tenure}
            {" "}
            months
          </strong>

        </div>


        <div className="detail-item">

          <span>
            Purpose
          </span>

          <strong>
            {application.loan_purpose}
          </strong>

        </div>


        <div className="detail-item">

          <span>
            Applied On
          </span>

          <strong>
            {application.application_date}
          </strong>

        </div>

      </div>

    </div>
  );
}


export default LatestApplication;