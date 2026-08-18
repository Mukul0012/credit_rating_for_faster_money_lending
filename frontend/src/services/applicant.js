import { apiRequest } from "../api/client";


export async function getMyProfile() {

  return apiRequest(
    "/api/applicant/me"
  );

}