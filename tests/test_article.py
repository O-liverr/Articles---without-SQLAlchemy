import pytest
from lib.models.article import Article
from lib.db.seed import seed_database

@pytest.fixture
def setup_database():
    from scripts.setup_db import setup_database
    setup_database()
    seed_database()

def test_article_initialization(setup_database):
    article = Article("Test Article", 1, 1)
    assert article.title == "Test Article"
    assert article.author_id == 1
    assert article.magazine_id == 1
    assert article.id is not None

def test_article_validation():
    with pytest.raises(ValueError):
        Article("", 1, 1)

def test_find_by_id(setup_database):
    article = Article.find_by_id(1)
    assert article.title == "Tech Trends 2025"

def test_find_by_title(setup_database):
    article = Article.find_by_title("Tech Trends 2025")
    assert article is not None
    assert article.id == 1