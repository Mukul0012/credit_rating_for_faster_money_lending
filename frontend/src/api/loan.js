import { apiRequest } from "./client";


export function assessLoan(data) {
  return apiRequest(
    "/api/loan/assess",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );
}


export function getLoanHistory() {
  return apiRequest(
    "/api/loan/history"
  );
}


export function getApplicationDetails(
  applicationId
) {
  return apiRequest(
    `/api/loan/application/${applicationId}`
  );
}