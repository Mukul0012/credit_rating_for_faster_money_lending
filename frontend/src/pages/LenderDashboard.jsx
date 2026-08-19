import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getPendingApplications, getAllApplications } from "../services/lender";
import { getLenderUser, lenderLogout } from "../services/lenderAuth";
import "../styles/lender-dashboard.css";

export default function LenderDashboard() {
  const navigate = useNavigate();
  const lenderUser = getLenderUser();

  const [activeTab, setActiveTab] = useState("pending");
  const [data, setData] = useState({
    applications: [],
    total_pending: 0,
    approved_today: 0,
    rejected_today: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  async function loadData(tab = activeTab) {
    try {
      setLoading(true);
      setError("");

      let result;
      if (tab === "pending") {
        result = await getPendingApplications();
      } else {
        result = await getAllApplications();
      }

      setData(result || { applications: [], total_pending: 0, approved_today: 0, rejected_today: 0 });
    } catch (err) {
      console.error("Error loading lender applications:", err);
      setError(err.message || "Failed to load applications");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData(activeTab);
  }, [activeTab]);

  function handleLogout() {
    lenderLogout();
    navigate("/lender/login", { replace: true });
  }

  const filteredApplications = (data.applications || []).filter((app) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      app.applicant_name?.toLowerCase().includes(q) ||
      String(app.application_id).includes(q) ||
      app.loan_purpose?.toLowerCase().includes(q) ||
      app.status?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="lender-dashboard-page">
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

      {/* DASHBOARD CONTAINER */}
      <div className="lender-dashboard-container">
        <div className="lender-dashboard-header">
          <div className="lender-header-text">
            <h1>Loan Application Queue</h1>
            <p>Assess applicant credit scores, inspect AI risk telemetry, and approve or reject loans.</p>
          </div>

          <button className="lender-refresh-btn" onClick={() => loadData(activeTab)} disabled={loading}>
            <span>↻</span> {loading ? "Refreshing..." : "Refresh Queue"}
          </button>
        </div>

        {/* STATS GRID */}
        <div className="lender-stats-grid">
          <div className="lender-stat-card pending">
            <div className="lender-stat-header">
              <span className="lender-stat-title">Pending Decisions</span>
              <div className="lender-stat-icon">⌛</div>
            </div>
            <div className="lender-stat-value">{data.total_pending ?? 0}</div>
            <div className="lender-stat-desc">Applications awaiting underwriter action</div>
          </div>

          <div className="lender-stat-card approved">
            <div className="lender-stat-header">
              <span className="lender-stat-title">Approved Today</span>
              <div className="lender-stat-icon">✓</div>
            </div>
            <div className="lender-stat-value">{data.approved_today ?? 0}</div>
            <div className="lender-stat-desc">Loans sanctioned today</div>
          </div>

          <div className="lender-stat-card rejected">
            <div className="lender-stat-header">
              <span className="lender-stat-title">Rejected Today</span>
              <div className="lender-stat-icon">✕</div>
            </div>
            <div className="lender-stat-value">{data.rejected_today ?? 0}</div>
            <div className="lender-stat-desc">Loans declined with feedback</div>
          </div>

          <div className="lender-stat-card total">
            <div className="lender-stat-header">
              <span className="lender-stat-title">Total in Queue</span>
              <div className="lender-stat-icon">📋</div>
            </div>
            <div className="lender-stat-value">{data.applications?.length ?? 0}</div>
            <div className="lender-stat-desc">Applications in current view</div>
          </div>
        </div>

        {/* APPLICATIONS TABLE PANEL */}
        <div className="lender-table-panel">
          <div className="lender-panel-controls">
            <div className="lender-filter-tabs">
              <button
                className={`lender-filter-btn ${activeTab === "pending" ? "active" : ""}`}
                onClick={() => setActiveTab("pending")}
              >
                Pending Review ({data.total_pending ?? 0})
              </button>
              <button
                className={`lender-filter-btn ${activeTab === "all" ? "active" : ""}`}
                onClick={() => setActiveTab("all")}
              >
                All Applications
              </button>
            </div>

            <div className="lender-search-box">
              <span className="lender-search-icon">🔍</span>
              <input
                type="text"
                placeholder="Search applicant, ID, purpose..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          {error && (
            <div className="lender-error" style={{ marginBottom: "20px" }}>
              <span>!</span>
              <div>{error}</div>
            </div>
          )}

          {loading ? (
            <div className="lender-empty-state">
              <div className="lender-empty-icon">⏳</div>
              <h3>Loading loan queue...</h3>
              <p>Fetching application metrics from database</p>
            </div>
          ) : filteredApplications.length === 0 ? (
            <div className="lender-empty-state">
              <div className="lender-empty-icon">✨</div>
              <h3>No applications in this queue</h3>
              <p>
                {activeTab === "pending"
                  ? "All pending loan applications have been processed."
                  : "No loan applications found matching your criteria."}
              </p>
            </div>
          ) : (
            <div className="lender-table-wrapper">
              <table className="lender-table">
                <thead>
                  <tr>
                    <th>App ID</th>
                    <th>Applicant</th>
                    <th>Loan Amount</th>
                    <th>Tenure</th>
                    <th>Purpose</th>
                    <th>Credit Score</th>
                    <th>ML Risk Level</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredApplications.map((app) => (
                    <tr key={app.application_id}>
                      <td>#{app.application_id}</td>
                      <td>
                        <div className="applicant-col">
                          <span className="applicant-name">{app.applicant_name}</span>
                          <span className="applicant-id">{app.applicant_email || `ID: ${app.applicant_id}`}</span>
                        </div>
                      </td>
                      <td>
                        <div className="amount-col">
                          <strong>₹{Number(app.loan_amount).toLocaleString("en-IN")}</strong>
                        </div>
                      </td>
                      <td>{app.loan_tenure ? `${app.loan_tenure} mo` : "N/A"}</td>
                      <td>{app.loan_purpose || "General"}</td>
                      <td>
                        {app.credit_score ? (
                          <span className={`score-badge grade-${(app.risk_grade || "c").toLowerCase()}`}>
                            ★ {app.credit_score} ({app.risk_grade || "N/A"})
                          </span>
                        ) : (
                          <span style={{ color: "#64748b" }}>N/A</span>
                        )}
                      </td>
                      <td>
                        {app.risk_level ? (
                          <span className={`lender-risk-badge ${app.risk_level.toLowerCase()}`}>
                            {app.risk_level}
                          </span>
                        ) : (
                          <span style={{ color: "#64748b" }}>Not Scored</span>
                        )}
                      </td>
                      <td>
                        <span
                          className={`lender-status-pill ${
                            app.status?.toLowerCase().replace(/\s+/g, "-") || "pending"
                          }`}
                        >
                          {app.status || "Pending"}
                        </span>
                      </td>
                      <td>
                        <button
                          className="lender-action-btn"
                          onClick={() => navigate(`/lender/review/${app.application_id}`)}
                        >
                          Assess Score →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
