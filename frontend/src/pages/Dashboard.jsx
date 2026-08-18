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


import {
  getLoanHistory
} from "../services/loan";


import {
  logout
} from "../services/auth";


import Sidebar
  from "../components/dashboard/Sidebar";

import StatCard
  from "../components/dashboard/StatCard";

import CreditScoreCard
  from "../components/dashboard/CreditScoreCard";

import LatestApplication
  from "../components/dashboard/LatestApplication";

import RiskAssessment
  from "../components/dashboard/RiskAssessment";

import ApplicationTable
  from "../components/dashboard/ApplicationTable";


import "../styles/dashboard.css";


function Dashboard() {

  const navigate =
    useNavigate();


  const [profile, setProfile] =
    useState(null);

  const [loanHistory, setLoanHistory] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  // =========================================
  // LOAD DASHBOARD DATA
  // =========================================

  useEffect(() => {

    async function loadDashboard() {

      try {

        setLoading(true);

        setError("");


        // -------------------------------------
        // APPLICANT PROFILE
        // -------------------------------------

        const profileData =
          await getMyProfile();


        setProfile(
          profileData
        );


        // -------------------------------------
        // LOAN HISTORY
        // -------------------------------------

        /*
         * Loan history is loaded separately.
         *
         * If the history endpoint fails,
         * the dashboard can still display
         * the applicant profile.
         */

        try {

          const historyData =
            await getLoanHistory();


          setLoanHistory(
            historyData?.applications || []
          );

        } catch (historyError) {

          console.error(
            "Loan history error:",
            historyError
          );

          setLoanHistory([]);

        }

      } catch (err) {

        console.error(
          "Dashboard error:",
          err
        );


        setError(
          err.message ||
          "Failed to load dashboard"
        );

      } finally {

        setLoading(false);

      }

    }


    loadDashboard();

  }, []);


  // =========================================
  // LOGOUT
  // =========================================

  function handleLogout() {

    logout();

    navigate("/login");

  }


  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (

      <div className="dashboard-loading">

        <div className="loading-spinner" />

        <p>
          Loading your dashboard...
        </p>

      </div>

    );

  }


  // =========================================
  // ERROR
  // =========================================

  if (error) {

    return (

      <div className="dashboard-error">

        <h2>
          Unable to load dashboard
        </h2>

        <p>
          {error}
        </p>


        <button
          onClick={handleLogout}
        >
          Logout
        </button>

      </div>

    );

  }


  // =========================================
  // DATA
  // =========================================

  const personal =
    profile?.personal || {};


  const employment =
    profile?.employment || {};


  const creditRating =
    profile?.credit_rating || {};


  const debtMetrics =
    profile?.debt_payment_metrics || {};


  const existingLoans =
    profile?.existing_loans || [];


  const latestApplication =
    profile?.latest_application ||
    profile?.application ||
    null;


  // =========================================
  // LATEST ASSESSED APPLICATION
  // =========================================

  /*
   * Loan history is expected to be newest first.
   *
   * Find the newest application that has
   * an assessment.
   */

  const latestAssessment =
    loanHistory.find(
      (application) =>
        application?.assessment_id !== null &&
        application?.assessment_id !== undefined
    );


  // =========================================
  // RENDER
  // =========================================

  return (

    <div className="dashboard-layout">


      {/* =====================================
          SIDEBAR
      ===================================== */}

      <Sidebar />


      {/* =====================================
          MAIN CONTENT
      ===================================== */}

      <main className="dashboard-main">


        {/* =====================================
            HEADER
        ===================================== */}

        <div className="dashboard-header">

          <div>

            <span className="eyebrow">
              OVERVIEW
            </span>


            <h1>

              Good to see you,{" "}

              {
                personal.full_name
                  ?.split(" ")[0] ||
                "Applicant"
              }

            </h1>


            <p>
              Here's an overview of your
              financial health and loan
              activity.
            </p>

          </div>


          <button
            className="primary-button"
            onClick={() =>
              navigate("/apply-loan")
            }
          >
            + New Loan Application
          </button>

        </div>


        {/* =====================================
            STAT CARDS
        ===================================== */}

        <div className="stats-grid">


          <StatCard

            title="Credit Score"

            value={
              creditRating.credit_score ??
              "N/A"
            }

            subtitle={
              `Grade ${
                creditRating.risk_grade ||
                "N/A"
              }`
            }

            icon="◉"

          />


          <StatCard

            title="Annual Income"

            value={
              employment.annual_income != null
                ? `₹${Number(
                    employment.annual_income
                  ).toLocaleString(
                    "en-IN"
                  )}`
                : "N/A"
            }

            subtitle={
              employment.employment_type ||
              "Employment"
            }

            icon="₹"

          />


          <StatCard

            title="Existing Loans"

            value={
              debtMetrics.existing_loans_count ??
              existingLoans.length ??
              0
            }

            subtitle="Active obligations"

            icon="▣"

          />


          <StatCard

            title="Applications"

            value={
              loanHistory.length
            }

            subtitle="Total applications"

            icon="↗"

          />

        </div>


        {/* =====================================
            CREDIT SCORE + LATEST APPLICATION
        ===================================== */}

        <div className="dashboard-two-column">


          <CreditScoreCard

            score={
              creditRating.credit_score
            }

            grade={
              creditRating.risk_grade
            }

          />


          <LatestApplication

            application={
              latestApplication
            }

          />

        </div>


        {/* =====================================
            RISK ASSESSMENT
        ===================================== */}

        {latestAssessment && (

          <RiskAssessment

            assessment={
              latestAssessment
            }

          />

        )}


        {/* =====================================
            APPLICATION HISTORY
        ===================================== */}

        <ApplicationTable

          applications={
            loanHistory
          }

        />


        {/* =====================================
            VIEW ALL APPLICATIONS
        ===================================== */}

        {loanHistory.length > 0 && (

          <div className="dashboard-view-all">

            <button
              className="secondary-button"
              onClick={() =>
                navigate("/loan-history")
              }
            >
              View All Loan Applications →
            </button>

          </div>

        )}

      </main>

    </div>

  );

}


export default Dashboard;