import { useEffect, useState } from "react";
import api from "../services/api";

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({
    name: "",
    code: "",
    description: ""
  });

  const [editingId, setEditingId] = useState(null);

  async function loadProjects() {
    const res = await api.get("/projects");
    setProjects(res.data);
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    if (editingId) {
      await api.patch(`/projects/${editingId}`, form);
      setEditingId(null);
    } else {
      await api.post("/projects", {
        ...form,
        status: "active"
      });
    }

    await api.post("/reports/refresh-materialized-view");

    setForm({ name: "", code: "", description: "" });
    loadProjects();
  }

  function handleEdit(project) {
    setEditingId(project.id);
    setForm({
      name: project.name,
      code: project.code,
      description: project.description || ""
    });
  }

  return (
    <div>
      <h2>Projects</h2>

      <div className="card">
        <h3>{editingId ? "Edit Project" : "Create Project"}</h3>

        <form onSubmit={handleSubmit}>
          <input
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />

          <input
            placeholder="Code"
            value={form.code}
            onChange={(e) => setForm({ ...form, code: e.target.value })}
          />

          <input
            placeholder="Description"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />

          <button className="primary-btn">
            {editingId ? "Update" : "Create"}
          </button>
        </form>
      </div>

      <div className="card">
        <h3>Project List</h3>

        {projects.map((p) => (
          <div key={p.id} className="list-item">
            <div>
              <strong>{p.name}</strong> ({p.code})
              <p className="subtle">{p.description}</p>
            </div>

            <button onClick={() => handleEdit(p)}>Edit</button>
          </div>
        ))}
      </div>
    </div>
  );
}