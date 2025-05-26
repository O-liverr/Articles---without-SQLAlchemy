import pytest
from lib.models.author import Author
from lib.db.seed import seed_database

@pytest.fixture
def setup_database():
    from scripts.setup_db import setup_database
    setup_database()
    seed_database()

def test_author_initialization(setup_database):
    author = Author("Test Author")
    assert author.name == "Test Author"
    assert author.id is not None

def test_author_name_validation():
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