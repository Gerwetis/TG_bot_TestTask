CREATE TABLE users (
    tg_id BIGINT PRIMARY KEY,
    username TEXT
);

CREATE TABLE storage (
    id SERIAL PRIMARY KEY,
    tg_id BIGINT REFERENCES users(tg_id) ON DELETE CASCADE,
    filename TEXT,
    path TEXT,
    file_type TEXT,
    uploaded_at TIMESTAMP
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    tg_id BIGINT,
    action TEXT,
    timestamp TIMESTAMP
);
