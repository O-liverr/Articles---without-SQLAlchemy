import pytest
from lib.models.magazine import Magazine
from lib.db.seed import seed_database
from scripts.setup_db import setup_database

@pytest.fixture
def setup_database():
    setup_database()
    seed_database()
    yield

def test_magazine_initialization(setup_database):
    magazine = Magazine("Test Mag", "Test Category")
    assert magazine.name == "Test Mag"
    assert magazine.category == "Test Category"
    assert magazine.id is not None

def test_magazine_validation(setup_database):
    with pytest.raises(ValueError):
        Magazine("", "Category")
    with pytest.raises(ValueError):
        Magazine("Name", "")

def test_magazine_articles(setup_database):
    magazine = Magazine.find_by_name("Tech Today")
    articles = magazine.articles()
    assert len(articles) >= 2
    assert any(article['title'] == "AI Revolution" for article in articles)

def test_magazine_contributors(setup_database):
    magazine = Magazine.find_by_name("Tech Today")
    contributors = magazine.contributors()
    assert any(author['name'] == "John Doe" for author in contributors)
    assert any(author['name'] == "Alice Johnson" for author in contributors)

def test_magazine_article_titles(setup_database):
    magazine = Magazine.find_by_name("Tech Today")
    titles = magazine.article_titles()
    assert "AI Revolution" in titles
    assert "Tech Trends" in titles

def test_magazine_top_publisher(setup_database):
    top_mag = Magazine.top_publisher()
    assert top_mag is not None
    assert top_mag.name in ["Tech Today", "Health Weekly", "Science Monthly"]