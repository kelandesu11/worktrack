import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

export default function WorkItemDetailsPage() {
  const { id } = useParams();

  const [item, setItem] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentBody, setCommentBody] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadDetails() {
    try {
      setLoading(true);

      const [itemRes, commentsRes] = await Promise.all([
        api.get(`/work-items/${id}`),
        api.get(`/work-items/${id}/comments`)
      ]);

      setItem(itemRes.data);
      setComments(commentsRes.data);
    } catch (err) {
      console.error("Failed to load work item details", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDetails();
  }, [id]);

  async function handleAddComment(e) {
    e.preventDefault();

    if (!commentBody.trim()) return;

    try {
      await api.post(`/work-items/${id}/comments`, {
        body: commentBody
      });
      setCommentBody("");
      loadDetails();
    } catch (err) {
      console.error("Failed to add comment", err);
    }
  }

  if (loading) return <p>Loading work item...</p>;

  if (!item) return <p>Work item not found.</p>;

  return (
    <div>
      <h2>Work Item Details</h2>

      <div className="card">
        <h3>{item.title}</h3>
        <p className="subtle">{item.description || "No description provided."}</p>

        <div className="detail-grid">
          <div>
            <strong>Status</strong>
            <p>{item.status}</p>
          </div>

          <div>
            <strong>Priority</strong>
            <p>{item.priority}</p>
          </div>

          <div>
            <strong>Project ID</strong>
            <p>{item.project_id}</p>
          </div>

          <div>
            <strong>Reporter ID</strong>
            <p>{item.reporter_id ?? "N/A"}</p>
          </div>

          <div>
            <strong>Assignee ID</strong>
            <p>{item.assignee_id ?? "N/A"}</p>
          </div>
        </div>

        {item.metadata_jsonb && (
          <div className="metadata-block">
            <strong>Metadata</strong>
            <pre>{JSON.stringify(item.metadata_jsonb, null, 2)}</pre>
          </div>
        )}
      </div>

      <div className="card">
        <h3>Add Comment</h3>

        <form onSubmit={handleAddComment}>
          <textarea
            rows="4"
            placeholder="Write a comment..."
            value={commentBody}
            onChange={(e) => setCommentBody(e.target.value)}
          />
          <button className="primary-btn">Add Comment</button>
        </form>
      </div>

      <div className="card">
        <h3>Comments</h3>

        {comments.length === 0 ? (
          <p className="subtle">No comments yet.</p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="comment-item">
              <p>{comment.body}</p>
              <p className="subtle">
                Author ID: {comment.author_id} | Comment ID: {comment.id}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}