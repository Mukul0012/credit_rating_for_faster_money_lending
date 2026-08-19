import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";


import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ApplyLoan from "./pages/ApplyLoan";
import ApplicationDetails from "./pages/ApplicationDetails";
import LoanHistory from "./pages/LoanHistory";
import CreditProfile from "./pages/CreditProfile";
import LenderLogin from "./pages/LenderLogin";
import LenderDashboard from "./pages/LenderDashboard";
import LenderReview from "./pages/LenderReview";

import { isAuthenticated } from "./services/auth";
import { isLenderAuthenticated } from "./services/lenderAuth";


function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function LenderProtectedRoute({ children }) {
  if (!isLenderAuthenticated()) {
    return <Navigate to="/lender/login" replace />;
  }
  return children;
}


function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* CUSTOMER PUBLIC */}

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

        {/* LENDER PUBLIC */}

        <Route
          path="/lender/login"
          element={<LenderLogin />}
        />

        {/* LENDER PROTECTED */}

        <Route
          path="/lender/dashboard"
          element={
            <LenderProtectedRoute>
              <LenderDashboard />
            </LenderProtectedRoute>
          }
        />

        <Route
          path="/lender/review/:applicationId"
          element={
            <LenderProtectedRoute>
              <LenderReview />
            </LenderProtectedRoute>
          }
        />


        {/* CUSTOMER PROTECTED */}

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