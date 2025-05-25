from lib.db.connection import get_connection

def run_example_queries():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        print("Magazines with at least 2 different authors:")
        cursor.execute("""
            SELECT m.name, COUNT(DISTINCT a.author_id) as author_count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING author_count >= 2
        """)
        for row in cursor.fetchall():
            print(f"{row['name']}: {row['author_count']} authors")
        
        print("\nAuthor with most articles:")
        cursor.execute("""
            SELECT a.name, COUNT(art.id) as article_count
            FROM authors a
            JOIN articles art ON a.id = art.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        print(f"{row['name']}: {row['article_count']} articles")
    except Exception as e:
        print(f"Query failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_example_queries()