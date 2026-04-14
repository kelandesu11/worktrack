INSERT INTO users (username, email, hashed_password, role)
VALUES
('admin', 'admin@example.com', '$2b$12$examplehash', 'admin'),
('member1', 'member1@example.com', '$2b$12$examplehash', 'member');

INSERT INTO projects (name, code, description, owner_id)
VALUES
('Internal Platform', 'INT-1', 'Main worktrack project', 1),
('Client Rollout', 'CL-1', 'Rollout work', 1);

INSERT INTO work_items (title, description, status, priority, project_id, assignee_id, reporter_id, metadata_jsonb)
VALUES
('Set up backend', 'Create FastAPI backend', 'in_progress', 'high', 1, 2, 1, '{"client_visible": true, "tags": ["backend", "api"]}'),
('Create dashboard', 'Prepare dashboard summary', 'todo', 'medium', 1, 2, 1, '{"client_visible": false, "tags": ["reporting"]}'),
('Prepare rollout notes', 'Document rollout steps', 'done', 'low', 2, 2, 1, '{"client_visible": true, "tags": ["ops"]}');

INSERT INTO comments (work_item_id, author_id, body)
VALUES
(1, 1, 'Initial backend scaffold started.'),
(1, 2, 'Working on auth now.');

INSERT INTO activity_logs (actor_id, work_item_id, event_type, event_payload_jsonb)
VALUES
(1, 1, 'work_item_created', '{"title": "Set up backend"}'),
(2, 1, 'comment_added', '{"comment": "Working on auth now."}');
