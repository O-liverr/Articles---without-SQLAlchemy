import pytest
from lib.models.author import Author

@pytest.fixture
def setup_database():
    import os
    from lib.db.connection import get_connection
    
    db_file = 'articles.db'
    if os.path.exists(db_file):
        os.remove(db_file)
    
    conn = get_connection()
    cursor = conn.cursor()
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM sqlite_sequence")
    authors = [("Jane Doe",), ("John Smith",), ("Alice Johnson",)]
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", authors)
    magazines = [("Tech Weekly", "Technology"), ("Fashion Monthly", "Fashion"), ("Science Digest", "Science")]
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)
    articles = [
        ("Tech Trends 2025", 1, 1),
        ("Fashion Forward", 2, 2),
        ("Quantum Breakthrough", 3, 3),
        ("AI Revolution", 1, 3),
        ("Style Guide", 2, 2)
    ]
    cursor.executemany("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles)
    
    conn.commit()
    conn.close()
    yield

def test_author_initialization(setup_database):
    author = Author("Test Author")
    assert author.name == "Test Author"
    assert author.id is not None

def test_author_name_validation(setup_database):
    with pytest.raises(ValueError):
        Author("")
    with pytest.raises(ValueError):
        Author(123)

def test_author_articles(setup_database):
    author = Author.find_by_id(1)
    articles = author.articles()
    assert len(articles) >= 1
    assert all(article.author_id == author.id for article in articles)

def test_author_magazines(setup_database):
    author = Author.find_by_id(1)
    magazines = author.magazines()
    assert len(magazines) >= 1

def test_add_article(setup_database):
    author = Author.find_by_id(1)
    from lib.models.magazine import Magazine
    magazine = Magazine.find_by_id(1)
    article = author.add_article(magazine, "New Article")
    assert article.title == "New Article"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id

def test_topic_areas(setup_database):
    author = Author.find_by_id(1)
    topics = author.topic_areas()
    assert len(topics) >= 1
    assert "Technology" in topics