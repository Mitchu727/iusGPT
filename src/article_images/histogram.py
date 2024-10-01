import json
import tiktoken
import matplotlib.pyplot as plt

from src.utils.utils import get_project_root
from statistics import mean


default_articles_source = get_project_root() / "documents" / "legal_acts" / "batch" / "civil_code" / "source.json"


def load_articles_as_documents(path=default_articles_source):
    with open(path, "r") as f:
        articles = json.load(f)
    documents = []
    for article in articles:
        # document = Document(page_content=article["content"].replace("\n", " "))
        documents.append(article["content"].replace("\n", " "))
    return documents



if __name__ == "__main__":
    docs = load_articles_as_documents()
    o200k_base_enc = tiktoken.get_encoding("o200k_base")
    # enc = tiktoken.encoding_for_model("gpt-4o")
    o200k_base_lengths = []
    for doc in docs:
        article_length = len(o200k_base_enc.encode(doc))
        o200k_base_lengths.append(article_length)

    (sorted(o200k_base_lengths, reverse=True))

    cl100k_base_enc = tiktoken.get_encoding("cl100k_base")
    cl100k_base_lengths = []
    for doc in docs:
        article_length = len(cl100k_base_enc.encode(doc))
        cl100k_base_lengths.append(article_length)

    context_sum = 0
    numerator = 0
    for value in sorted(cl100k_base_lengths, reverse=True):
        if context_sum < 15835:
            context_sum += value
            numerator += 1
        else:
            break
    print(numerator)

    context_sum = 0
    numerator = 0
    for value in sorted(cl100k_base_lengths, reverse=False):
        if context_sum < 15835:
            context_sum += value
            numerator += 1
        else:
            break
    print(numerator)

    print(sum(cl100k_base_lengths)/len(cl100k_base_lengths))
    print(sum(o200k_base_lengths)/len(o200k_base_lengths))
    # # print(lengths)
    # # print(len(lengths))
    # # print(mean(lengths))
    # plt.figure(figsize=(6, 3))
    # plt.subplot(1, 2, 1)
    # plt.hist(cl100k_base_lengths, bins = 50)
    # plt.title("cl100k_base encoder")
    # plt.xticks([0, 200, 400, 600, 800, 1000])
    # plt.subplot(1, 2, 2)
    # plt.hist(o200k_base_lengths, bins = 50)
    # plt.title("o200k_base encoder")
    # plt.xticks([0, 200, 400, 600, 800, 1000])
    # # plt.show()
    # plt.savefig("histogram.pdf")