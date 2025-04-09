CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    disabled BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_users_username ON users (username);

CREATE TABLE IF NOT EXISTS email_folders (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    username VARCHAR NOT NULL
);

CREATE INDEX idx_email_folders_username ON email_folders (username);

CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    subject VARCHAR NOT NULL,
    content TEXT NOT NULL,
    sender VARCHAR NOT NULL,
    recipients VARCHAR NOT NULL,
    folder_id INTEGER REFERENCES email_folders(id) ON DELETE CASCADE
);

INSERT INTO email_folders (name, username) VALUES ('Main Folder', 'admin');

INSERT INTO emails (subject, content, sender, recipients, folder_id)
VALUES ('First message', 'Hello!', 'admin', 'user', 1);

INSERT INTO users (username, email, hashed_password, disabled)
VALUES
    ('admin', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE),
    ('user', 'user@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE);
