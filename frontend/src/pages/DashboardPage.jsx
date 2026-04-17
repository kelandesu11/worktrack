import { useEffect, useState } from "react";
import api from "../services/api";

export default function DashboardPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get("/dashboard/summary");
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  if (loading) return <p>Loading dashboard...</p>;

  return (
    <div>
      <h2>Dashboard</h2>

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