import { useEffect, useState } from "react";
import api from "../services/api";

export default function DashboardPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadDashboard() {
    try {
      const res = await api.get("/dashboard/summary");
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) return <p>Loading dashboard...</p>;

  return (
    <div>
      <div className="page-header">
        <h2>Dashboard</h2>
        <button
          className="secondary-btn"
          onClick={async () => {
            setLoading(true);
            await api.post("/reports/refresh-materialized-view");
            await loadDashboard();
          }}
        >
          Refresh Dashboard
        </button>
      </div>

      <div className="grid">
        {data.map((item) => (
          <div key={item.project_id} className="card">
            <h3>{item.project_name}</h3>
            <p>Total: {item.total_work_items}</p>
            <p>Open: {item.open_work_items}</p>
            <p>Done: {item.done_work_items}</p>
            <p>High Priority: {item.high_priority_items}</p>
          </div>
        ))}
      </div>
    </div>
  );
}