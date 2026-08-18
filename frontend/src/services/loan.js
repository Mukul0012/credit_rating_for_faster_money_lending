import { apiRequest } from "../api/client";


/**
 * Get all loan applications
 */
export async function getLoanHistory() {

  return apiRequest(
    "/api/loan/history"
  );

}


/**
 * Get a single application
 */
export async function getApplicationDetails(
  applicationId
) {

  return apiRequest(
    `/api/loan/application/${applicationId}`
  );

}


/**
 * Submit a new loan application
 *
 * The backend gets applicant_id
 * from the authenticated user.
 */
export async function assessLoan(
  loanData
) {

  return apiRequest(
    "/api/loan/assess",
    {
      method: "POST",

      body: JSON.stringify(
        loanData
      ),
    }
  );

}