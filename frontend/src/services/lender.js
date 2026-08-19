import { getLenderToken, lenderLogout } from "./lenderAuth";

const API_BASE_URL = "http://127.0.0.1:8000";

async function lenderRequest(endpoint, options = {}) {
  const token = getLenderToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  let data = null;
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    data = await response.json();
  }

  if (response.status === 401) {
    lenderLogout();
    if (window.location.pathname !== "/lender/login") {
      window.location.href = "/lender/login";
    }
    throw new Error("Lender session expired. Please sign in again.");
  }

  if (!response.ok) {
    throw new Error(
      data?.detail || data?.message || "Lender request failed"
    );
  }

  return data;
}

/**
 * Fetch pending loan applications for lender
 */
export async function getPendingApplications() {
  return lenderRequest("/api/lender/pending-applications");
}

/**
 * Fetch all loan applications for lender
 */
export async function getAllApplications() {
  return lenderRequest("/api/lender/all-applications");
}

/**
 * Fetch full application details for assessment review
 */
export async function getApplicationForReview(applicationId) {
  return lenderRequest(`/api/lender/application/${applicationId}`);
}

/**
 * Submit lender decision (APPROVE / REJECT)
 */
export async function submitDecision(applicationId, decision, rejectionReason = null) {
  return lenderRequest(`/api/lender/application/${applicationId}/decide`, {
    method: "POST",
    body: JSON.stringify({
      decision,
      rejection_reason: rejectionReason,
    }),
  });
}
