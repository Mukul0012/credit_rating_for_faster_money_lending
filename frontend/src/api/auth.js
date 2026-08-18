import { apiRequest } from "./client";

export async function login(
  applicantId,
  password
) {
  const formData =
    new URLSearchParams();

  formData.append(
    "username",
    applicantId
  );

  formData.append(
    "password",
    password
  );

  const response = await fetch(
    `${import.meta.env.VITE_API_URL}/api/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
      body: formData,
    }
  );

  const data =
    await response.json();

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Login failed"
    );
  }

  localStorage.setItem(
    "access_token",
    data.access_token
  );

  return data;
}

export function logout() {
  localStorage.removeItem(
    "access_token"
  );
}