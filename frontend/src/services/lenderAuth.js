const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Login lender
 */
export async function lenderLogin(email, password) {
  const response = await fetch(
    `${API_BASE_URL}/api/lender/login`,
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
      "Lender login failed"
    );
  }

  if (data.access_token) {
    localStorage.setItem(
      "lender_token",
      data.access_token
    );
    localStorage.setItem(
      "lender_user",
      JSON.stringify({
        lender_id: data.lender_id,
        full_name: data.full_name,
        email: data.email
      })
    );
  }

  return data;
}

/**
 * Register new lender
 */
export async function lenderRegister(email, password, fullName) {
  const response = await fetch(
    `${API_BASE_URL}/api/lender/register`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
        full_name: fullName,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Lender registration failed"
    );
  }

  if (data.access_token) {
    localStorage.setItem(
      "lender_token",
      data.access_token
    );
    localStorage.setItem(
      "lender_user",
      JSON.stringify({
        lender_id: data.lender_id,
        full_name: data.full_name,
        email: data.email
      })
    );
  }

  return data;
}

/**
 * Get Lender JWT token
 */
export function getLenderToken() {
  return localStorage.getItem("lender_token");
}

/**
 * Get Lender user profile
 */
export function getLenderUser() {
  try {
    const raw = localStorage.getItem("lender_user");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

/**
 * Check if lender is authenticated
 */
export function isLenderAuthenticated() {
  return Boolean(getLenderToken());
}

/**
 * Logout lender
 */
export function lenderLogout() {
  localStorage.removeItem("lender_token");
  localStorage.removeItem("lender_user");
}
