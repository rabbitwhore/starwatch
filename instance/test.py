import sqlite3

conn = sqlite3.connect('domains.db')
cursor = conn.cursor()

create_table_statement = """
CREATE TABLE IF NOT EXISTS domains (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    available VARCHAR(100),
    registrar VARCHAR(100),
    creation_date VARCHAR(100),
    updated_date VARCHAR(100),
    transfer_date VARCHAR(100),
    expiration_date VARCHAR(100),
    name_servers VARCHAR(255),
    last_updated VARCHAR(255)
)   
"""

cursor.execute(create_table_statement)
conn.commit()

cursor.close()
conn.close()