import { Link, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function AppLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">WorkTrack</div>

        <nav className="nav-links">
          <Link
            to="/dashboard"
            className={location.pathname === "/dashboard" ? "active" : ""}
          >
            Dashboard
          </Link>

          <Link
            to="/projects"
            className={location.pathname === "/projects" ? "active" : ""}
          >
            Projects
          </Link>

          <Link
            to="/work-items"
            className={location.pathname === "/work-items" ? "active" : ""}
          >
            Work Items
          </Link>
        </nav>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <div>
            <h1>WorkTrack Frontend</h1>
            <p className="subtle">
              Logged in as {user?.username || user?.email || "User"}
            </p>
          </div>

          <button className="secondary-btn" onClick={logout}>
            Logout
          </button>
        </header>

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}