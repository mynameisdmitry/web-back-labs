CREATE TABLE IF NOT EXISTS offices (
    number INTEGER PRIMARY KEY,
    tenant TEXT NOT NULL DEFAULT '',
    price INTEGER NOT NULL
);

INSERT OR IGNORE INTO offices (number, tenant, price) VALUES
(1,'',903),(2,'',906),(3,'',909),(4,'',912),(5,'',915),
(6,'',918),(7,'',921),(8,'',924),(9,'',927),(10,'',930);