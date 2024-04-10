import itertools
import json

from src.tag_determiner import TagDeterminer


def flat_and_unique(list_of_lists):
    return list(set(itertools.chain(*list_of_lists)))

input_path = "../documents/civilCodeSplitted/codex_tagged.json"

with open(input_path, "r") as f:
    codex = json.load(f)

tags_lists = []
for chapter in codex:
    tags_lists.append(chapter["chapter_tag_summarized"])

final_tags_lists = flat_and_unique(tags_lists)
print(len(final_tags_lists))
print(final_tags_lists)

tag_determiner = TagDeterminer()
question = "Czym jest gospodarstwo rolne?"
determined_tags = tag_determiner.determine_tags(question, final_tags_lists)
print(determined_tags)