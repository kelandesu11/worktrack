SELECT w.id, w.title, p.name AS project_name, u.username AS assignee
FROM work_items w
JOIN projects p ON p.id = w.project_id
LEFT JOIN users u ON u.id = w.assignee_id;

SELECT p.name, COUNT(w.id) AS total_items
FROM projects p
LEFT JOIN work_items w ON w.project_id = p.id
GROUP BY p.id, p.name
HAVING COUNT(w.id) >= 1;

WITH status_counts AS (
    SELECT status, COUNT(*) AS total
    FROM work_items
    WHERE is_deleted = FALSE
    GROUP BY status
)
SELECT * FROM status_counts ORDER BY total DESC;

SELECT *
FROM work_items
WHERE project_id IN (
    SELECT id FROM projects WHERE status = 'active'
);
