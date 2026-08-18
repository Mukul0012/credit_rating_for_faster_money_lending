import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { assessLoan } from "../services/loan";

import "../styles/apply-loan.css";


function ApplyLoan() {

  const navigate = useNavigate();


  const [form, setForm] = useState({
    loan_amount: "",
    loan_tenure: "",
    loan_purpose: "",
  });


  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  // =========================================
  // HANDLE INPUT CHANGE
  // =========================================

  function handleChange(event) {

    const {
      name,
      value
    } = event.target;


    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));


    if (error) {
      setError("");
    }

  }


  // =========================================
  // SUBMIT APPLICATION
  // =========================================

  async function handleSubmit(event) {

    event.preventDefault();


    if (loading) {
      return;
    }


    setError("");


    const loanAmount =
      Number(form.loan_amount);

    const loanTenure =
      Number(form.loan_tenure);

    const loanPurpose =
      form.loan_purpose.trim();


    // =======================================
    // VALIDATION
    // =======================================

    if (
      !Number.isFinite(loanAmount) ||
      loanAmount <= 0
    ) {

      setError(
        "Please enter a valid loan amount."
      );

      return;
    }


    if (
      loanAmount % 1000 !== 0
    ) {

      setError(
        "Loan amount must be in multiples of ₹1,000."
      );

      return;
    }


    if (
      !Number.isFinite(loanTenure) ||
      loanTenure <= 0
    ) {

      setError(
        "Please select a valid loan tenure."
      );

      return;
    }


    if (!loanPurpose) {

      setError(
        "Please select a loan purpose."
      );

      return;
    }


    // =======================================
    // SUBMIT TO BACKEND
    // =======================================

    try {

      setLoading(true);


      /*
       * applicant_id is intentionally NOT sent.
       *
       * FastAPI identifies the applicant from
       * the authenticated JWT.
       */

      const result =
        await assessLoan({

          loan_amount: loanAmount,

          loan_tenure: loanTenure,

          loan_purpose: loanPurpose,

        });


      console.log(
        "Loan assessment result:",
        result
      );


      // =====================================
      // GET APPLICATION ID
      // =====================================

      /*
       * Supports both possible response shapes:
       *
       * {
       *   application_id: 105
       * }
       *
       * OR:
       *
       * {
       *   application: {
       *     application_id: 105
       *   }
       * }
       */

      const applicationId =
        result?.application_id ??
        result?.application?.application_id;


      if (!applicationId) {

        console.error(
          "Unexpected backend response:",
          result
        );

        throw new Error(
          "Application was processed, but no application ID was returned."
        );

      }


      // =====================================
      // REDIRECT
      // =====================================

      /*
       * Do NOT pass assessment data through
       * React Router state.
       *
       * ApplicationDetails.jsx will fetch
       * fresh data from:
       *
       * GET /api/loan/application/{id}
       */

      navigate(
        `/application/${applicationId}`,
        {
          replace: true
        }
      );


    } catch (err) {

      console.error(
        "Loan assessment error:",
        err
      );


      setError(
        err.message ||
        "Unable to process your loan application. Please try again."
      );

    } finally {

      setLoading(false);

    }

  }


  // =========================================
  // UI
  // =========================================

  return (

    <div className="apply-loan-page">

      <div className="apply-loan-container">


        {/* =================================
            HEADER
        ================================= */}

        <div className="apply-loan-header">

          <button
            type="button"
            className="back-button"
            onClick={() =>
              navigate("/dashboard")
            }
            disabled={loading}
          >
            ← Dashboard
          </button>


          <span className="apply-eyebrow">
            NEW APPLICATION
          </span>


          <h1>
            Apply for a Loan
          </h1>


          <p>
            Enter the details of your new
            loan request. Your existing
            financial history will be
            automatically considered during
            the credit assessment.
          </p>

        </div>


        {/* =================================
            MAIN CONTENT
        ================================= */}

        <div className="apply-layout">


          {/* =================================
              FORM
          ================================= */}

          <div className="apply-form-card">

            <div className="apply-card-header">

              <span className="apply-eyebrow">
                LOAN DETAILS
              </span>

              <h2>
                Tell us about your loan
              </h2>

            </div>


            <form
              onSubmit={handleSubmit}
              noValidate
            >


              {/* =============================
                  LOAN AMOUNT
              ============================== */}

              <div className="form-group">

                <label htmlFor="loan_amount">
                  Loan Amount
                </label>


                <div className="input-with-prefix">

                  <span>
                    ₹
                  </span>


                  <input
                    id="loan_amount"
                    name="loan_amount"
                    type="number"
                    min="1000"
                    step="1000"
                    placeholder="e.g. 300000"
                    value={
                      form.loan_amount
                    }
                    onChange={
                      handleChange
                    }
                    disabled={loading}
                    required
                  />

                </div>


                <small>
                  Enter the loan amount in
                  multiples of ₹1,000.
                </small>

              </div>


              {/* =============================
                  LOAN TENURE
              ============================== */}

              <div className="form-group">

                <label htmlFor="loan_tenure">
                  Loan Tenure
                </label>


                <select
                  id="loan_tenure"
                  name="loan_tenure"
                  value={
                    form.loan_tenure
                  }
                  onChange={
                    handleChange
                  }
                  disabled={loading}
                  required
                >

                  <option value="">
                    Select tenure
                  </option>

                  <option value="12">
                    12 months
                  </option>

                  <option value="24">
                    24 months
                  </option>

                  <option value="36">
                    36 months
                  </option>

                  <option value="48">
                    48 months
                  </option>

                  <option value="60">
                    60 months
                  </option>

                  <option value="72">
                    72 months
                  </option>

                  <option value="84">
                    84 months
                  </option>

                </select>


                <small>
                  Select the repayment period.
                </small>

              </div>


              {/* =============================
                  LOAN PURPOSE
              ============================== */}

              <div className="form-group">

                <label htmlFor="loan_purpose">
                  Loan Purpose
                </label>


                <select
                  id="loan_purpose"
                  name="loan_purpose"
                  value={
                    form.loan_purpose
                  }
                  onChange={
                    handleChange
                  }
                  disabled={loading}
                  required
                >

                  <option value="">
                    Select purpose
                  </option>

                  <option value="Personal">
                    Personal
                  </option>

                  <option value="Home Loan">
                    Home Loan
                  </option>

                  <option value="Education">
                    Education
                  </option>

                  <option value="Medical">
                    Medical
                  </option>

                  <option value="Vehicle">
                    Vehicle
                  </option>

                  <option value="Business">
                    Business
                  </option>

                  <option value="Other">
                    Other
                  </option>

                </select>

              </div>


              {/* =============================
                  ERROR
              ============================== */}

              {error && (

                <div className="apply-error">

                  <span>
                    !
                  </span>


                  <p>
                    {error}
                  </p>

                </div>

              )}


              {/* =============================
                  SUBMIT
              ============================== */}

              <button
                type="submit"
                className="assess-button"
                disabled={loading}
              >

                {loading ? (

                  <>
                    <span className="button-spinner" />

                    Assessing your application...
                  </>

                ) : (

                  <>
                    Assess Credit Risk →
                  </>

                )}

              </button>


              {/* =============================
                  DISCLAIMER
              ============================== */}

              <p className="form-disclaimer">

                Your existing credit history,
                income, debt obligations and
                repayment behaviour will be
                considered automatically.

              </p>

            </form>

          </div>


          {/* =================================
              INFORMATION PANEL
          ================================= */}

          <div className="assessment-info">


            <div className="info-card">

              <div className="info-icon">
                ✓
              </div>


              <h3>
                Automated Assessment
              </h3>


              <p>
                Our machine learning model
                evaluates your application
                using your existing financial
                profile.
              </p>

            </div>


            <div className="info-card">

              <div className="info-icon">
                ◉
              </div>


              <h3>
                Risk Analysis
              </h3>


              <p>
                You'll receive an approval
                probability, risk score,
                risk level and key risk
                factors.
              </p>

            </div>


            <div className="info-card">

              <div className="info-icon">
                →
              </div>


              <h3>
                What happens next?
              </h3>


              <p>
                Your application and
                assessment are saved so you
                can view them later from
                Applications.
              </p>

            </div>

          </div>

        </div>

      </div>

    </div>

  );

}


export default ApplyLoan;