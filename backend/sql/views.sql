CREATE OR REPLACE VIEW project_workload_view AS
SELECT
    p.id AS project_id,
    p.name AS project_name,
    COUNT(w.id) AS total_work_items
FROM projects p
LEFT JOIN work_items w ON w.project_id = p.id AND w.is_deleted = FALSE
GROUP BY p.id, p.name;
