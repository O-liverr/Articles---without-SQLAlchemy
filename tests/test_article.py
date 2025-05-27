import pytest
from lib.models.article import Article

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

def test_article_initialization(setup_database):
    article = Article("Test Article", 1, 1)
    assert article.title == "Test Article"
    assert article.author_id == 1
    assert article.magazine_id == 1
    assert article.id is not None

def test_article_validation(setup_database):
    with pytest.raises(ValueError):
        Article("", 1, 1)

def test_find_by_id(setup_database):
    article = Article.find_by_id(1)
    assert article is not None
    assert article.title == "Tech Trends 2025"

def test_find_by_title(setup_database):
    article = Article.find_by_title("Tech Trends 2025")
    assert article is not None
    assert article.id == 1