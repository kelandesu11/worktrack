import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function WorkItemsPage() {
  const [items, setItems] = useState([]);
  const [projects, setProjects] = useState([]);

  const [form, setForm] = useState({
    title: "",
    description: "",
    project_id: "",
    status: "todo",
    priority: "medium"
  });

  const [editingId, setEditingId] = useState(null);

  const [filters, setFilters] = useState({
    status: "",
    priority: "",
    search: ""
  });

  async function loadProjects() {
    const res = await api.get("/projects");
    setProjects(res.data);
  }

  async function loadItems() {
    if (filters.search) {
      const res = await api.get(`/work-items/search?q=${filters.search}`);
      setItems(res.data);
      return;
    }

    const params = {};
    if (filters.status) params.status = filters.status;
    if (filters.priority) params.priority = filters.priority;

    const res = await api.get("/work-items", { params });
    setItems(res.data);
  }

  useEffect(() => {
    loadProjects();
    loadItems();
  }, []);

  useEffect(() => {
    loadItems();
  }, [filters]);

  async function handleSubmit(e) {
    e.preventDefault();

    if (editingId) {
      await api.patch(`/work-items/${editingId}`, {
        ...form,
        project_id: Number(form.project_id)
      });
      setEditingId(null);
    } else {
      await api.post("/work-items", {
        ...form,
        project_id: Number(form.project_id)
      });
    }

    setForm({
      title: "",
      description: "",
      project_id: "",
      status: "todo",
      priority: "medium"
    });

    loadItems();
  }

  function handleEdit(item) {
    setEditingId(item.id);
    setForm({
      title: item.title,
      description: item.description || "",
      project_id: String(item.project_id),
      status: item.status,
      priority: item.priority
    });
  }

  return (
    <div>
      <h2>Work Items</h2>

      <div className="card">
        <h3>Filters</h3>

        <input
          placeholder="Search..."
          value={filters.search}
          onChange={(e) =>
            setFilters({ ...filters, search: e.target.value })
          }
        />

        <select
          value={filters.status}
          onChange={(e) =>
            setFilters({ ...filters, status: e.target.value })
          }
        >
          <option value="">All Status</option>
          <option value="todo">Todo</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>

        <select
          value={filters.priority}
          onChange={(e) =>
            setFilters({ ...filters, priority: e.target.value })
          }
        >
          <option value="">All Priority</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <div className="card">
        <h3>{editingId ? "Edit Work Item" : "Create Work Item"}</h3>

        <form onSubmit={handleSubmit}>
          <input
            placeholder="Title"
            value={form.title}
            onChange={(e) =>
              setForm({ ...form, title: e.target.value })
            }
          />

          <input
            placeholder="Description"
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
          />

          <select
            value={form.project_id}
            onChange={(e) =>
              setForm({ ...form, project_id: e.target.value })
            }
          >
            <option value="">Select Project</option>
            {projects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>

          <select
            value={form.status}
            onChange={(e) =>
              setForm({ ...form, status: e.target.value })
            }
          >
            <option value="todo">Todo</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>

          <select
            value={form.priority}
            onChange={(e) =>
              setForm({ ...form, priority: e.target.value })
            }
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <button className="primary-btn">
            {editingId ? "Update" : "Create"}
          </button>
        </form>
      </div>

      <div className="card">
        <h3>Work Items</h3>

        {items.length === 0 ? (
          <p className="subtle">No work items found.</p>
        ) : (
          items.map((item) => (
            <div key={item.id} className="list-item">
              <div>
                <Link to={`/work-items/${item.id}`} className="item-link">
                  <strong>{item.title}</strong>
                </Link>
                <p className="subtle">
                  {item.status} | {item.priority}
                </p>
              </div>

              <button onClick={() => handleEdit(item)}>Edit</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}