import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("accessToken") || "");
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      localStorage.setItem("accessToken", token);
      loadMe();
    } else {
      localStorage.removeItem("accessToken");
      setUser(null);
      setLoading(false);
    }
  }, [token]);

  async function loadMe() {
    try {
      const response = await api.get("/auth/me");
      setUser(response.data);
    } catch (error) {
      console.error("Failed to load user", error);
      setToken("");
    } finally {
      setLoading(false);
    }
  }

  async function login(username_or_email, password) {
    const response = await api.post("/auth/login", {
      username_or_email,
      password
    });

    if (response.data.access_token) {
      setToken(response.data.access_token);
      return { success: true };
    }

    return { success: false };
  }

  function logout() {
    setToken("");
    setUser(null);
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: Boolean(token),
      login,
      logout
    }),
    [token, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}