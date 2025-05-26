from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def cli():
    print("Articles Code Challenge CLI")
    while True:
        print("\nOptions: 1) List authors 2) List magazines 3) Find articles by author 4) Exit")
        choice = input("Choose an option (1-4): ")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if choice == "1":
                cursor.execute("SELECT name FROM authors")
                print("Authors:", [row['name'] for row in cursor.fetchall()])
            elif choice == "2":
                cursor.execute("SELECT name FROM magazines")
                print("Magazines:", [row['name'] for row in cursor.fetchall()])
            elif choice == "3":
                name = input("Enter author name: ")
                author = Author.find_by_name(name)
                if author:
                    articles = author.articles()
                    print(f"Articles by {name}:", [a['title'] for a in articles])
                else:
                    print("Author not found.")
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    cli()