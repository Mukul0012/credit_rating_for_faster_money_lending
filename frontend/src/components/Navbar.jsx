import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";


export default function Navbar() {

  const {
    logout
  } = useAuth();

  const navigate =
    useNavigate();


  function handleLogout() {

    logout();

    navigate("/login");
  }


  return (
    <nav className="navbar">

      <Link
        to="/dashboard"
        className="logo"
      >
        CreditFlow
      </Link>


      <div className="nav-links">

        <Link to="/dashboard">
          Dashboard
        </Link>

        <Link to="/apply">
          New Assessment
        </Link>

        <button
          onClick={
            handleLogout
          }
        >
          Logout
        </button>

      </div>

    </nav>
  );
}