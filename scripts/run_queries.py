from lib.models.author import Author
from lib.models.magazine import Magazine

def run_example_queries():
    author = Author.find_by_name("Jane Doe")
    if author:
        print(f"Articles by {author.name}:")
        for article in author.articles():
            print(f"- {article.title}")
        
        print(f"\nMagazines contributed to by {author.name}:")
        for mag in author.magazines():
            print(f"- {mag.name} ({mag.category})")
    
    magazine = Magazine.find_by_name("Tech Weekly")
    if magazine:
        print(f"\nArticles in {magazine.name}:")
        for title in magazine.article_titles():
            print(f"- {title}")
        
        print(f"\nContributors to {magazine.name}:")
        for contributor in magazine.contributors():
            print(f"- {contributor.name}")

if __name__ == "__main__":
    run_example_queries()