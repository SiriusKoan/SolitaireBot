CREATE TABLE IF NOT EXISTS games (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    rounds  INTEGER NOT NULL    DEFAULT 0
);