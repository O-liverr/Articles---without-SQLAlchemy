import pytest
from lib.models.magazine import Magazine

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

def test_magazine_initialization(setup_database):
    magazine = Magazine("Test Mag", "Test Cat")
    assert magazine.name == "Test Mag"
    assert magazine.category == "Test Cat"
    assert magazine.id is not None

def test_magazine_validations(setup_database):
    with pytest.raises(ValueError):
        Magazine("", "Category")
    with pytest.raises(ValueError):
        Magazine("Name", "")

def test_magazine_articles(setup_database):
    magazine = Magazine.find_by_id(1)
    articles = magazine.articles()
    assert len(articles) >= 1
    assert all(article.magazine_id == magazine.id for article in articles)

def test_magazine_contributors(setup_database):
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributors()
    assert len(contributors) >= 1

def test_article_titles(setup_database):
    magazine = Magazine.find_by_id(1)
    titles = magazine.article_titles()
    assert len(titles) >= 1
    assert "Tech Trends 2025" in titles

def test_top_publisher(setup_database):
    top_mag = Magazine.top_publisher()
    assert top_mag is not None
    assert isinstance(top_mag, Magazine)

def test_contributing_authors(setup_database):
    magazine = Magazine.find_by_id(2)
    contributors = magazine.contributing_authors()
    assert len(contributors) == 0