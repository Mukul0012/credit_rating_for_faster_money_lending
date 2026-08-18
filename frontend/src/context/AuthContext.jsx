import {
  createContext,
  useContext,
  useState
} from "react";

import {
  login as loginApi,
  logout as logoutApi
} from "../api/auth";


const AuthContext =
  createContext(null);


export function AuthProvider({
  children
}) {

  const [
    isAuthenticated,
    setIsAuthenticated
  ] = useState(
    Boolean(
      localStorage.getItem(
        "access_token"
      )
    )
  );


  async function login(
    applicantId,
    password
  ) {

    await loginApi(
      applicantId,
      password
    );

    setIsAuthenticated(true);
  }


  function logout() {

    logoutApi();

    setIsAuthenticated(false);
  }


  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {

  return useContext(
    AuthContext
  );
}