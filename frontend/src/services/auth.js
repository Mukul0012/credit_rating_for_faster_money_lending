const API_BASE_URL = "http://127.0.0.1:8000";


/**
 * Login applicant
 */
export async function login(email, password) {

  const response = await fetch(
    `${API_BASE_URL}/api/auth/login`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        email,
        password,
      }),
    }
  );


  const data = await response.json();


  if (!response.ok) {

    throw new Error(
      data.detail ||
      "Login failed"
    );

  }


  if (data.access_token) {

    localStorage.setItem(
      "access_token",
      data.access_token
    );

  }


  return data;
}


/**
 * Register new applicant
 */
export async function register(
  applicantId,
  password
) {

  const response = await fetch(
    `${API_BASE_URL}/api/auth/register`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        applicant_id: Number(applicantId),
        password,
      }),
    }
  );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(
      data.detail ||
      "Registration failed"
    );

  }


  return data;
}


/**
 * Get JWT token
 */
export function getToken() {

  return localStorage.getItem(
    "access_token"
  );

}


/**
 * Check authentication
 */
export function isAuthenticated() {

  return Boolean(
    getToken()
  );

}


/**
 * Logout
 */
export function logout() {

  localStorage.removeItem(
    "access_token"
  );

}