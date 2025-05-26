import pytest
from lib.models.magazine import Magazine
from lib.db.seed import seed_database

@pytest.fixture
def setup_database():
    from scripts.setup_db import setup_database
    setup_database()
    seed_database()

def test_magazine_initialization(setup_database):
    magazine = Magazine("Test Mag", "Test Cat")
    assert magazine.name == "Test Mag"
    assert magazine.category == "Test Cat"
    assert magazine.id is not None

def test_magazine_validations():
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