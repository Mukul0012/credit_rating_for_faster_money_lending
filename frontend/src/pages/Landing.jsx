import {
  useNavigate
} from "react-router-dom";

import {
  isAuthenticated
} from "../services/auth";

import "../styles/landing.css";


function Landing() {

  const navigate =
    useNavigate();


  function handleGetStarted() {

    if (isAuthenticated()) {

      navigate("/dashboard");

    } else {

      navigate("/register");

    }

  }


  return (

    <div className="landing-page">


      {/* =====================================
          NAVBAR
      ===================================== */}

      <nav className="landing-nav">

        <div
          className="landing-brand"
          onClick={() =>
            navigate("/")
          }
        >

          <div className="landing-logo">
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


        <div className="landing-nav-actions">

          <button
            className="landing-login"
            onClick={() =>
              navigate("/login")
            }
          >
            Sign in
          </button>


          <button
            className="landing-nav-button"
            onClick={() =>
              navigate("/register")
            }
          >
            Get Started
          </button>

        </div>

      </nav>


      {/* =====================================
          HERO
      ===================================== */}

      <main>


        <section className="landing-hero">


          <div className="landing-hero-content">

            <div className="landing-pill">

              <span>
                ●
              </span>

              AI-powered credit assessment

            </div>


            <h1>

              Smarter credit decisions.

              <span>
                Faster lending.
              </span>

            </h1>


            <p>

              Assess loan applications using
              intelligent credit-risk analysis,
              existing financial data and
              machine learning — all in one
              streamlined platform.

            </p>


            <div className="landing-hero-actions">

              <button
                className="landing-primary-button"
                onClick={handleGetStarted}
              >
                Start your application

                <span>
                  →
                </span>

              </button>


              <button
                className="landing-secondary-button"
                onClick={() =>
                  navigate("/login")
                }
              >
                Already a customer?
              </button>

            </div>


            <div className="landing-trust">

              <div>
                <span>✓</span>
                Secure authentication
              </div>

              <div>
                <span>✓</span>
                Automated risk analysis
              </div>

              <div>
                <span>✓</span>
                Transparent decisions
              </div>

            </div>

          </div>


          {/* =================================
              HERO VISUAL
          ================================= */}

          <div className="landing-visual">

            <div className="dashboard-preview">


              <div className="preview-top">

                <div>

                  <span>
                    CREDIT PROFILE
                  </span>

                  <strong>
                    Financial Overview
                  </strong>

                </div>

                <div className="preview-avatar">
                  A
                </div>

              </div>


              <div className="preview-score">

                <div>

                  <span>
                    Credit Score
                  </span>

                  <strong>
                    742
                  </strong>

                  <small>
                    Grade A
                  </small>

                </div>


                <div className="preview-ring">

                  <div>
                    85%
                  </div>

                </div>

              </div>


              <div className="preview-metrics">

                <div>
                  <span>
                    Annual Income
                  </span>

                  <strong>
                    ₹8.4L
                  </strong>
                </div>


                <div>
                  <span>
                    Debt-to-Income
                  </span>

                  <strong>
                    24%
                  </strong>
                </div>


                <div>
                  <span>
                    Payment History
                  </span>

                  <strong>
                    96%
                  </strong>
                </div>

              </div>


              <div className="preview-assessment">

                <div className="preview-check">
                  ✓
                </div>

                <div>

                  <strong>
                    Risk assessment complete
                  </strong>

                  <span>
                    Low risk · High confidence
                  </span>

                </div>

                <span className="preview-approved">
                  APPROVED
                </span>

              </div>

            </div>


            <div className="floating-card floating-one">

              <span>
                Approval probability
              </span>

              <strong>
                86.4%
              </strong>

            </div>


            <div className="floating-card floating-two">

              <span className="floating-dot">
                ●
              </span>

              Assessment completed

            </div>

          </div>

        </section>


        {/* =====================================
            FEATURES
        ===================================== */}

        <section className="landing-features">

          <div className="landing-section-heading">

            <span>
              BUILT FOR FASTER LENDING
            </span>

            <h2>
              Everything you need to make
              better credit decisions.
            </h2>

          </div>


          <div className="feature-grid">


            <Feature
              icon="◉"
              title="Intelligent Risk Scoring"
              description="Evaluate credit risk using a machine-learning powered assessment engine."
            />


            <Feature
              icon="↗"
              title="Instant Assessment"
              description="Submit a loan request and receive risk metrics without repetitive data entry."
            />


            <Feature
              icon="✓"
              title="Transparent Decisions"
              description="Understand approval probability, risk level and the factors influencing an assessment."
            />


            <Feature
              icon="▣"
              title="Complete Financial View"
              description="Bring income, existing loans, debt obligations and credit information together."
            />

          </div>

        </section>


        {/* =====================================
            CTA
        ===================================== */}

        <section className="landing-cta">

          <div>

            <span>
              READY TO GET STARTED?
            </span>

            <h2>
              Your next loan application
              starts here.
            </h2>

            <p>
              Create your account and get
              access to your personalized
              credit dashboard.
            </p>

          </div>


          <button
            onClick={() =>
              navigate("/register")
            }
          >
            Create your account →
          </button>

        </section>

      </main>


      {/* =====================================
          FOOTER
      ===================================== */}

      <footer className="landing-footer">

        <div className="landing-brand">

          <div className="landing-logo">
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


        <p>
          Intelligent credit assessment
          for faster lending decisions.
        </p>

      </footer>

    </div>

  );
}


/* =========================================
   FEATURE COMPONENT
========================================= */

function Feature({
  icon,
  title,
  description
}) {

  return (

    <div className="landing-feature">

      <div className="feature-icon">
        {icon}
      </div>

      <h3>
        {title}
      </h3>

      <p>
        {description}
      </p>

    </div>

  );

}


export default Landing;