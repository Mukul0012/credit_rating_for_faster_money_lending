import {
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import {
  register
} from "../services/auth";

import "../styles/auth.css";


function Register() {

  const navigate =
    useNavigate();


  const [form, setForm] = useState({
    applicant_id: "",
    password: "",
    confirm_password: "",
  });


  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");


  function handleChange(event) {

    const {
      name,
      value
    } = event.target;


    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));


    setError("");
    setSuccess("");

  }


  async function handleSubmit(event) {

    event.preventDefault();

    setError("");
    setSuccess("");


    const applicantId =
      Number(form.applicant_id);

    const password =
      form.password;

    const confirmPassword =
      form.confirm_password;


    // =========================================
    // VALIDATION
    // =========================================

    if (
      !form.applicant_id ||
      !Number.isInteger(applicantId) ||
      applicantId <= 0
    ) {

      setError(
        "Please enter a valid Applicant ID."
      );

      return;

    }


    if (!password) {

      setError(
        "Please enter a password."
      );

      return;

    }


    if (password.length < 6) {

      setError(
        "Password must contain at least 6 characters."
      );

      return;

    }


    if (
      password !== confirmPassword
    ) {

      setError(
        "Passwords do not match."
      );

      return;

    }


    // =========================================
    // REGISTER
    // =========================================

    try {

      setLoading(true);


      await register(
        applicantId,
        password
      );


      setSuccess(
        "Account created successfully. Redirecting to login..."
      );


      setTimeout(() => {

        navigate("/login");

      }, 1200);


    } catch (err) {

      console.error(
        "Registration error:",
        err
      );


      setError(
        err.message ||
        "Unable to create your account."
      );

    } finally {

      setLoading(false);

    }

  }


  return (

    <div className="auth-page">


      {/* =====================================
          BRAND
      ===================================== */}

      <div
        className="auth-brand"
        onClick={() =>
          navigate("/")
        }
      >

        <div className="auth-logo">
          CR
        </div>

        <div>

          <strong>
            CreditRisk
          </strong>

          <span>
            Faster Lending
          </span>

        </div>

      </div>


      {/* =====================================
          CARD
      ===================================== */}

      <div className="auth-card">


        <div className="auth-header">

          <span className="auth-eyebrow">
            GET STARTED
          </span>

          <h1>
            Create your account
          </h1>

          <p>
            Use your Applicant ID to create
            your secure CreditRisk account.
          </p>

        </div>


        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >


          {/* =================================
              APPLICANT ID
          ================================= */}

          <div className="auth-field">

            <label htmlFor="applicant_id">
              Applicant ID
            </label>

            <input
              id="applicant_id"
              name="applicant_id"
              type="number"
              min="1"
              placeholder="e.g. 1"
              value={
                form.applicant_id
              }
              onChange={
                handleChange
              }
              disabled={loading}
              required
            />

          </div>


          {/* =================================
              PASSWORD
          ================================= */}

          <div className="auth-field">

            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              name="password"
              type="password"
              placeholder="Minimum 6 characters"
              value={
                form.password
              }
              onChange={
                handleChange
              }
              disabled={loading}
              autoComplete="new-password"
              required
            />

          </div>


          {/* =================================
              CONFIRM PASSWORD
          ================================= */}

          <div className="auth-field">

            <label htmlFor="confirm_password">
              Confirm Password
            </label>

            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              placeholder="Re-enter your password"
              value={
                form.confirm_password
              }
              onChange={
                handleChange
              }
              disabled={loading}
              autoComplete="new-password"
              required
            />

          </div>


          {/* =================================
              ERROR
          ================================= */}

          {error && (

            <div className="auth-message auth-error">

              <span>
                !
              </span>

              {error}

            </div>

          )}


          {/* =================================
              SUCCESS
          ================================= */}

          {success && (

            <div className="auth-message auth-success">

              <span>
                ✓
              </span>

              {success}

            </div>

          )}


          {/* =================================
              SUBMIT
          ================================= */}

          <button
            className="auth-submit"
            type="submit"
            disabled={loading}
          >

            {loading ? (

              <>
                <span className="auth-spinner" />

                Creating account...
              </>

            ) : (

              <>
                Create Account

                <span>
                  →
                </span>
              </>

            )}

          </button>

        </form>


        {/* =================================
            LOGIN
        ================================= */}

        <div className="auth-divider">

          <span>
            Already have an account?
          </span>

        </div>


        <button
          className="auth-secondary-button"
          onClick={() =>
            navigate("/login")
          }
        >
          Sign in instead
        </button>


        <button
          className="auth-home-link"
          onClick={() =>
            navigate("/")
          }
        >
          ← Back to home
        </button>

      </div>


      <p className="auth-footer">
        Secure credit assessment platform
      </p>

    </div>

  );

}


export default Register;