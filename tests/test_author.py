import pytest
from lib.models.author import Author
from lib.db.seed import seed_database
from scripts.setup_db import setup_database

@pytest.fixture
def setup_database():
    setup_database()
    seed_database()

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
    author = Author.find_by_name("John Doe")
    articles = author.articles()
    assert len(articles) >= 2
    assert any(article['title'] == "AI Revolution" for article in articles)

def test_author_magazines(setup_database):
    author = Author.find_by_name("John Doe")
    magazines = author.magazines()
    assert any(magazine['name'] == "Tech Today" for magazine in magazines)
    assert any(magazine['name'] == "Science Monthly" for magazine in magazines)

def test_author_topic_areas(setup_database):
    author = Author.find_by_name("John Doe")
    categories = author.topic_areas()
    assert "Technology" in categories
    assert "Science" in categories

def test_author_add_article(setup_database):
    author = Author.find_by_name("John Doe")
    from lib.models.magazine import Magazine
    magazine = Magazine.find_by_name("Tech Today")
    article = author.add_article(magazine, "New Article")
    assert article.title == "New Article"
    assert article.author.name == "John Doe"
    assert article.magazine.name == "Tech Today"