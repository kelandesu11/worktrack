INSERT INTO projects (name, code, description, owner_id)
VALUES ('Ops Dashboard', 'OPS-1', 'Ops team project', 1);

SELECT * FROM projects ORDER BY id DESC;

UPDATE work_items
SET status = 'done', actual_hours = 6
WHERE id = 1;

DELETE FROM comments
WHERE id = 999;
