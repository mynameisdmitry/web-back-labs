
-- SQLite variant
CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    title_ru TEXT NOT NULL,
    year INTEGER NOT NULL,
    description TEXT NOT NULL
);

-- Postgres variant (uncomment if applying to Postgres)
-- CREATE TABLE IF NOT EXISTS films (
--     id SERIAL PRIMARY KEY,
--     title TEXT NOT NULL,
--     title_ru TEXT NOT NULL,
--     year INTEGER NOT NULL,
--     description TEXT NOT NULL
-- );
