import {
  getToken,
  logout
} from "../services/auth";


const API_BASE_URL =
  "http://127.0.0.1:8000";


export async function apiRequest(
  endpoint,
  options = {}
) {

  const token =
    getToken();


  const headers = {

    "Content-Type":
      "application/json",

    ...(options.headers || {}),

  };


  if (token) {

    headers.Authorization =
      `Bearer ${token}`;

  }


  const response =
    await fetch(
      `${API_BASE_URL}${endpoint}`,
      {
        ...options,
        headers
      }
    );


  // =========================================
  // HANDLE EMPTY RESPONSE
  // =========================================

  let data = null;

  const contentType =
    response.headers.get(
      "content-type"
    );


  if (
    contentType &&
    contentType.includes(
      "application/json"
    )
  ) {

    data =
      await response.json();

  }


  // =========================================
  // UNAUTHORIZED
  // =========================================

  if (response.status === 401) {

    logout();

    /*
     * Redirect directly because this can happen
     * from any protected API request.
     */

    if (
      window.location.pathname !==
      "/login"
    ) {

      window.location.href =
        "/login";

    }


    throw new Error(
      "Your session has expired. Please login again."
    );

  }


  // =========================================
  // OTHER API ERRORS
  // =========================================

  if (!response.ok) {

    throw new Error(
      data?.detail ||
      data?.message ||
      "API request failed"
    );

  }


  return data;

}