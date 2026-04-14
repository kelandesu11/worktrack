CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_summary_mv AS
SELECT
    p.id AS project_id,
    p.name AS project_name,
    COUNT(w.id) AS total_work_items,
    COUNT(*) FILTER (WHERE w.status != 'done' AND w.id IS NOT NULL AND w.is_deleted = FALSE) AS open_work_items,
    COUNT(*) FILTER (WHERE w.status = 'done' AND w.id IS NOT NULL AND w.is_deleted = FALSE) AS done_work_items,
    COUNT(*) FILTER (WHERE w.priority = 'high' AND w.id IS NOT NULL AND w.is_deleted = FALSE) AS high_priority_items
FROM projects p
LEFT JOIN work_items w ON w.project_id = p.id
GROUP BY p.id, p.name;

REFRESH MATERIALIZED VIEW dashboard_summary_mv;
