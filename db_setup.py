import sqlite3

conn = sqlite3.connect('graph.db')
c = conn.cursor()

# Create tables
c.execute('''
    CREATE TABLE IF NOT EXISTS nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_node TEXT,
        to_node TEXT,
        distance REAL
    )
''')

conn.commit()
conn.close()
