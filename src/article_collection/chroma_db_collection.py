import chromadb
from src.article_collection.embeddings import sentence_transformer

chroma_client = chromadb.PersistentClient()


def print_results(results):
    for article in results['documents'][0]:
        print(article)


def load_civil_code_articles(codex_file = "../../documents/civilCodeTxtGenerated/kodeks.txt"):
    with open(codex_file, "r") as f:
        articles = f.readlines()
    return articles


def generate_ids(articles_list):
    return list(map(lambda tup: f"id{tup[0]}", enumerate(articles_list)))


def get_civil_code_collection(
        create_new=False,
        codex_file="../../documents/civilCodeTxtGenerated/kodeks.txt",
        collection_name="civil_code"
):
    if create_new:
        civil_code_collection = chroma_client.create_collection(name=collection_name)
    else:
        civil_code_collection = chroma_client.get_or_create_collection(name=collection_name)
    articles = load_civil_code_articles(codex_file)
    ids = generate_ids(articles)
    civil_code_collection.add(
        embeddings=sentence_transformer(articles),
        documents=articles,
        ids=ids
    )
    return civil_code_collection