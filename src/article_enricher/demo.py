from src.article_enricher.article_enricher_agent import ArticleEnricherAgent
from src.secrets import OPEN_API_KEY
import os
import json
queries = [
    "Czym jest gospodarstwo rolne?",
    "Jaka jest definicja nieruchomości?",
    "Komu przysługuje własność stanowiąca mienie państwowe?",
    "Czy gospodarstwo rolne może składać się z samych budynków?",
    "Czym jest wyzysk?",
    "Kiedy można uchylić się od złożonego oświadczenia woli?"
]

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

if __name__ == "__main__":
    article_enricher_agent = ArticleEnricherAgent()
    experiments = []
    for query in queries:
        response = article_enricher_agent.enrich_with_articles(query, 100)
        case = {}
        case["query"] = query
        case["answer"] = response
        print("<-PYTANIE->")
        print(query)
        print("<-ODPOWIEDŹ->")
        print(response)
        experiments.append(case.copy())

    with open('experiments.json', 'w') as f:
        json.dump(experiments, f)



    # print(response)