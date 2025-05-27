import os
from lib.db.connection import get_connection

def setup_database():
    
    db_file = 'articles.db'
    if os.path.exists(db_file):
        os.remove(db_file)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    
    conn.commit()
    conn.close()
    print("Database schema created successfully.")

if __name__ == "__main__":
    setup_database()