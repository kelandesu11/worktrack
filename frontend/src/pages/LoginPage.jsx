import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState({
    username_or_email: "",
    password: ""
  });

  const [error, setError] = useState("");

  const from = location.state?.from?.pathname || "/dashboard";

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      const result = await login(form.username_or_email, form.password);

      if (result.success) {
        navigate(from, { replace: true });
      } else {
        setError("Invalid login");
      }
    } catch (err) {
      setError("Login failed");
    }
  }

  return (
    <div className="center-page">
      <div className="card auth-card">
        <h2>Login</h2>

        <form onSubmit={handleSubmit}>
          <input
            placeholder="Email or Username"
            value={form.username_or_email}
            onChange={(e) =>
              setForm({ ...form, username_or_email: e.target.value })
            }
          />

          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />

          {error && <p className="error">{error}</p>}

          <button type="submit" className="primary-btn">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}