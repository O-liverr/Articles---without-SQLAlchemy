import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database
from scripts.setup_db import setup_database

@pytest.fixture
def setup_database():
    setup_database()
    seed_database()

def test_article_initialization(setup_database):
    author = Author.find_by_name("John Doe")
    magazine = Magazine.find_by_name("Tech Today")
    article = Article("Test Article", author, magazine)
    assert article.title == "Test Article"
    assert article.author.name == "John Doe"
    assert article.magazine.name == "Tech Today"
    assert article.id is not None

def test_article_validation(setup_database):
    author = Author.find_by_name("John Doe")
    magazine = Magazine.find_by_name("Tech Today")
    with pytest.raises(ValueError):
        Article("", author, magazine)
    with pytest.raises(ValueError):
        Article("Title", Author("No ID"), magazine)  # Author not in DB

def test_article_find_by_id(setup_database):
    article = Article.find_by_title("AI Revolution")
    assert article is not None
    assert article.title == "AI Revolution"
    assert article.author.name == "John Doe"