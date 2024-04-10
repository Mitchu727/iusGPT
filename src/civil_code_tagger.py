import json
input_path = "../documents/civilCodeSplitted/kodeks.json"
cache_path = "../documents/civilCodeSplitted/cache.json"
output_path = "../documents/civilCodeSplitted/codex_tagged.json"
from src.article_tagger import DummyArticleTagger, ChatGPT35ArticleTagger
import itertools


def determine_chapter_tags_summarized(chapter_to_summarize):
    articles_tags = chapter_to_summarize["articles_tags"]
    chapter_tag = chapter_to_summarize["chapter_tag"]
    return list(set(itertools.chain(*articles_tags, chapter_tag)))

with open(input_path, "r") as f:
    codex = json.load(f)

# article_tagger = DummyArticleTagger()
article_tagger = ChatGPT35ArticleTagger()

# print(chapter_one)
for chapter in codex:
    article_tags = []
    for article in chapter["articles"]:
        article_tags.append(article_tagger.tag_article(article))
    chapter["articles_tags"] = article_tags
    chapter["chapter_tag"] = article_tagger.tag_article(chapter["id"])
    chapter["chapter_tag_summarized"] = determine_chapter_tags_summarized(chapter)
    print(chapter["id"])
    with open(cache_path, "a") as f:
        json.dump(chapter, f)
# print(article_tags)

with open(output_path, "w") as f:
    json.dump(codex, f)