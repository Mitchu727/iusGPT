import json
input_path = "../documents/civilCodeSplitted/kodeks.json"
cache_path = "../documents/civilCodeSplitted/cache.json"
output_path = "../documents/civilCodeSplitted/articles_tagged.json"
from src.tagger import DummyTagger, ChatGPT35Tagger
import itertools


def determine_chapter_tags_summarized(chapter_to_summarize):
    articles_tags = chapter_to_summarize["articles_tags"]
    chapter_tag = chapter_to_summarize["chapter_tag"]
    return list(set(itertools.chain(*articles_tags, chapter_tag)))

with open(input_path, "r") as f:
    codex = json.load(f)

# article_tagger = DummyArticleTagger()
tagger = ChatGPT35Tagger()

results = []
for chapter in codex[:2]:
    for article in chapter["articles"]:
        result = {
            article: tagger.tag_text(article)
        }
        results.append(result)

print(len(tagger.get_tags()))
print(tagger.get_tags())

with open(output_path, "w") as f:
    json.dump(results, f)

# # print(chapter_one)
# for chapter in codex:
#     content = chapter["id"] + "\n" +  "".join(chapter["articles"])
#     tags = tagger.tag_text(content)
#     chapter["chapter_tag_summarized"] = tags
#     with open(cache_path, "a") as f:
#         json.dump(chapter, f)
#     print(chapter["id"])
#     print(tags)
# # print(article_tags)
#
# with open(output_path, "w") as f:
#     json.dump(codex, f)