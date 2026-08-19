import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { lenderLogin, lenderRegister } from "../services/lenderAuth";
import "../styles/lender-auth.css";

export default function LenderLogin() {
  const navigate = useNavigate();
  const [isRegister, setIsRegister] = useState(false);

  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (error) setError("");
  }

  function handleDemoFill() {
    setForm({
      email: "underwriter@bank.com",
      password: "password123",
      full_name: "Sarah Jenkins (Senior Underwriter)",
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (loading) return;

    setError("");
    setSuccess("");

    if (!form.email || !form.password) {
      setError("Please fill in all required fields.");
      return;
    }

    if (isRegister && !form.full_name) {
      setError("Please enter your full name.");
      return;
    }

    try {
      setLoading(true);

      if (isRegister) {
        await lenderRegister(form.email, form.password, form.full_name);
        setSuccess("Registration successful! Logging in...");
      } else {
        await lenderLogin(form.email, form.password);
      }

      navigate("/lender/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Authentication failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="lender-auth-page">
      <div className="lender-auth-brand" onClick={() => navigate("/")}>
        <div className="lender-auth-logo">LP</div>
        <div>
          <strong>CreditFlow</strong>
          <span>Lender Portal</span>
        </div>
      </div>

      <div className="lender-auth-card">
        <div className="lender-auth-header">
          <span className="lender-portal-badge">UNDERWRITER & LENDER ACCESS</span>
          <h1>{isRegister ? "Register Lender Account" : "Sign In to Lender Portal"}</h1>
          <p>
            {isRegister
              ? "Create institutional credentials to assess and decision loan applications."
              : "Review loan applications, evaluate risk metrics, and make lending decisions."}
          </p>
        </div>

        <div className="lender-tabs">
          <button
            type="button"
            className={`lender-tab-btn ${!isRegister ? "active" : ""}`}
            onClick={() => {
              setIsRegister(false);
              setError("");
            }}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`lender-tab-btn ${isRegister ? "active" : ""}`}
            onClick={() => {
              setIsRegister(true);
              setError("");
            }}
          >
            Register
          </button>
        </div>

        <form className="lender-auth-form" onSubmit={handleSubmit}>
          {isRegister && (
            <div className="lender-field">
              <label htmlFor="full_name">Full Name & Title</label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                placeholder="e.g. Sarah Jenkins (Senior Underwriter)"
                value={form.full_name}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>
          )}

          <div className="lender-field">
            <label htmlFor="email">Work Email</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="underwriter@bank.com"
              value={form.email}
              onChange={handleChange}
              disabled={loading}
              required
            />
          </div>

          <div className="lender-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              disabled={loading}
              required
            />
          </div>

          {error && (
            <div className="lender-error">
              <span>!</span>
              <div>{error}</div>
            </div>
          )}

          {success && (
            <div className="lender-success">
              <span>✓</span>
              <div>{success}</div>
            </div>
          )}

          <button type="submit" className="lender-submit" disabled={loading}>
            {loading
              ? isRegister
                ? "Creating Account..."
                : "Signing In..."
              : isRegister
              ? "Create Lender Account →"
              : "Sign In as Lender →"}
          </button>
        </form>

        <div className="lender-auth-footer">
          <button
            type="button"
            className="lender-customer-link"
            onClick={handleDemoFill}
          >
            Prefill Demo Credentials
          </button>

          <button
            type="button"
            className="lender-customer-link"
            onClick={() => navigate("/login")}
          >
            ← Switch to Applicant / Customer Portal
          </button>
        </div>
      </div>
    </div>
  );
}
