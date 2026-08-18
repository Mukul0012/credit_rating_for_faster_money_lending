import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";


import Landing
  from "./pages/Landing";

import Login
  from "./pages/Login";

import Register
  from "./pages/Register";

import Dashboard
  from "./pages/Dashboard";

import ApplyLoan
  from "./pages/ApplyLoan";

import ApplicationDetails
  from "./pages/ApplicationDetails";

import LoanHistory
  from "./pages/LoanHistory";

import CreditProfile
  from "./pages/CreditProfile";

import {
  isAuthenticated
} from "./services/auth";


function ProtectedRoute({
  children
}) {

  if (!isAuthenticated()) {

    return (
      <Navigate
        to="/login"
        replace
      />
    );

  }

  return children;

}


function App() {

  return (

    <BrowserRouter>

      <Routes>


        {/* PUBLIC */}

        <Route
          path="/"
          element={<Landing />}
        />


        <Route
          path="/login"
          element={<Login />}
        />


        <Route
          path="/register"
          element={<Register />}
        />


        {/* PROTECTED */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />


        <Route
          path="/apply-loan"
          element={
            <ProtectedRoute>
              <ApplyLoan />
            </ProtectedRoute>
          }
        />


        <Route
          path="/loan-history"
          element={
            <ProtectedRoute>
              <LoanHistory />
            </ProtectedRoute>
          }
        />


        <Route
          path="/credit-profile"
          element={
            <ProtectedRoute>
              <CreditProfile />
            </ProtectedRoute>
          }
        />


        <Route
          path="/application/:applicationId"
          element={
            <ProtectedRoute>
              <ApplicationDetails />
            </ProtectedRoute>
          }
        />


        {/* FALLBACK */}

        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>

    </BrowserRouter>

  );

}


export default App;