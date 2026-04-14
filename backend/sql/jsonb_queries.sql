SELECT *
FROM work_items
WHERE metadata_jsonb->>'client_visible' = 'true';

SELECT *
FROM work_items
WHERE metadata_jsonb->'tags' @> '["backend"]'::jsonb;

SELECT *
FROM activity_logs
WHERE event_payload_jsonb->>'field_changed' = 'status';
