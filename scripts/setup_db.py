from lib.db.connection import get_connection

def setup_database():
    conn = get_connection()
    try:
        with open('lib/db/schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        print("Database schema created successfully.")
    except Exception as e:
        print(f"Error setting up database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()