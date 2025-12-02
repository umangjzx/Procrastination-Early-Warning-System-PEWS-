import sqlite3

conn = sqlite3.connect("behavior.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    tab_switches INTEGER,
    scroll_speed REAL,
    idle_time INTEGER,
    mouse_distance REAL,
    url_category TEXT,
    label INTEGER  -- 1 = distraction, 0 = focused, NULL = unlabeled
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    score REAL
);
""")

conn.commit()
conn.close()

print("Database initialized: behavior.db")
