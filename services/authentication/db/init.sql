CREATE DATABASE app_users;
use app_users;

CREATE TABLE IF NOT EXISTS all_users (id VARCHAR(20) PRIMARY KEY, password VARCHAR(1024) NOT NULL, user_role VARCHAR(10) NOT NULL);

INSERT INTO all_users (id, password, user_role)
VALUES
('ecs_ny', 'iloveny', 'store'),
('james', 'password', 'user'),
('admin', 'admin', 'admin');
