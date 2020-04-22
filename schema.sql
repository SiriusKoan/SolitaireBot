CREATE TABLE IF NOT EXISTS room (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    word    TEXT    NOT NULL,  -- the last word
    players TEXT    NOT NULL,  -- split players with ';', like '@aaa;@bbb;@ccc'
    status  BOOLEAN NOT NULL    DEFAULT FALSE,
    rounds  INTEGER NOT NULL    DEFAULT 0
);