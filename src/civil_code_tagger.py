import json
input_path = "../documents/civilCodeSplitted/kodeks.json"
cache_path = "../documents/civilCodeSplitted/cache.json"
from src.article_tagger import DummyArticleTagger, ChatGPT35ArticleTagger


with open(input_path, "r") as f:
    codex = json.load(f)

article_tagger = DummyArticleTagger()
# v2_article_tagger = ChatGPT35ArticleTagger()
chapter_one = codex[0]
article = chapter_one["articles"][0]
print(article)
# tags = v2_article_tagger.tag_article(article)
# print(tags)

# print(chapter_one)
article_tags = []
tagged_chapters = []
for article in chapter_one["articles"]:
    article_tags.append(article_tagger.tag_article(article))

chapter_one["article_tags"] = article_tags

with open(cache_path, "w+") as f:
    json.dumps(codex, f)
print(codex[0])
# print(article_tags)