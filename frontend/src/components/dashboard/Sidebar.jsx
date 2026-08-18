import {
  NavLink,
  useNavigate
} from "react-router-dom";

import {
  logout
} from "../../services/auth";

import "./Sidebar.css";


function Sidebar() {

  const navigate =
    useNavigate();


  function handleLogout() {

    logout();

    navigate("/login", {
      replace: true
    });

  }


  return (

    <aside className="dashboard-sidebar">

      {/* =====================================
          BRAND
      ===================================== */}

      <div className="sidebar-brand">

        <div className="sidebar-logo">
          CR
        </div>

        <div>

          <strong>
            CreditRisk
          </strong>

          <span>
            Lending Platform
          </span>

        </div>

      </div>


      {/* =====================================
          NAVIGATION
      ===================================== */}

      <nav className="sidebar-navigation">

        <span className="sidebar-label">
          MENU
        </span>


        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `sidebar-link ${
              isActive
                ? "active"
                : ""
            }`
          }
        >
          <span className="sidebar-icon">
            ◉
          </span>

          <span>
            Dashboard
          </span>
        </NavLink>


        <NavLink
          to="/credit-profile"
          className={({ isActive }) =>
            `sidebar-link ${
              isActive
                ? "active"
                : ""
            }`
          }
        >
          <span className="sidebar-icon">
            ◈
          </span>

          <span>
            Credit Profile
          </span>
        </NavLink>


        <NavLink
          to="/loan-history"
          className={({ isActive }) =>
            `sidebar-link ${
              isActive
                ? "active"
                : ""
            }`
          }
        >
          <span className="sidebar-icon">
            ▣
          </span>

          <span>
            Loan History
          </span>
        </NavLink>


        <NavLink
          to="/apply-loan"
          className={({ isActive }) =>
            `sidebar-link ${
              isActive
                ? "active"
                : ""
            }`
          }
        >
          <span className="sidebar-icon">
            +
          </span>

          <span>
            Apply for Loan
          </span>
        </NavLink>

      </nav>


      {/* =====================================
          BOTTOM
      ===================================== */}

      <div className="sidebar-bottom">

        <button
          className="sidebar-logout"
          onClick={handleLogout}
        >

          <span className="sidebar-icon">
            ↪
          </span>

          <span>
            Logout
          </span>

        </button>

      </div>

    </aside>

  );

}


export default Sidebar;