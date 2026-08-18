import {
  useState
} from "react";

import {
  useNavigate
} from "react-router-dom";

import {
  login
} from "../services/auth";

import "../styles/auth.css";


function Login() {

  const navigate =
    useNavigate();


  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleSubmit(event) {

    event.preventDefault();

    setError("");


    if (!email.trim()) {

      setError(
        "Please enter your email address."
      );

      return;
    }


    if (!password) {

      setError(
        "Please enter your password."
      );

      return;
    }


    try {

      setLoading(true);


      await login(
        email.trim(),
        password
      );


      navigate("/dashboard", {
        replace: true,
      });


    } catch (err) {

      console.error(
        "Login error:",
        err
      );


      setError(
        err.message ||
        "Invalid email or password."
      );

    } finally {

      setLoading(false);

    }

  }


  return (

    <div className="auth-page">


      {/* BRAND */}

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


      {/* CARD */}

      <div className="auth-card">


        <div className="auth-header">

          <span className="auth-eyebrow">
            WELCOME BACK
          </span>

          <h1>
            Sign in to your account
          </h1>

          <p>
            Access your credit dashboard,
            applications and financial profile.
          </p>

        </div>


        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >


          {/* EMAIL */}

          <div className="auth-field">

            <label htmlFor="email">
              Email Address
            </label>

            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) => {

                setEmail(
                  event.target.value
                );

                setError("");

              }}
              disabled={loading}
              autoComplete="email"
            />

          </div>


          {/* PASSWORD */}

          <div className="auth-field">

            <div className="auth-label-row">

              <label htmlFor="password">
                Password
              </label>

            </div>

            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => {

                setPassword(
                  event.target.value
                );

                setError("");

              }}
              disabled={loading}
              autoComplete="current-password"
            />

          </div>


          {/* ERROR */}

          {error && (

            <div className="auth-message auth-error">

              <span>
                !
              </span>

              {error}

            </div>

          )}


          {/* SUBMIT */}

          <button
            className="auth-submit"
            type="submit"
            disabled={loading}
          >

            {loading ? (

              <>
                <span className="auth-spinner" />

                Signing in...
              </>

            ) : (

              <>
                Sign In
                <span>→</span>
              </>

            )}

          </button>

        </form>


        <div className="auth-divider">
          <span>New to CreditRisk?</span>
        </div>


        <button
          className="auth-secondary-button"
          onClick={() =>
            navigate("/register")
          }
        >
          Create an account
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


export default Login;