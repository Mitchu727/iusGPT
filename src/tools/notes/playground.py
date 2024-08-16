from src.utils.utils import extract_id_from_article_content

path = "civil_code_annotated.txt"
with open(path, "r") as f:
    lines = f.readlines()

def remove_id_from_article(article_content):
    article_id = extract_id_from_article_content(article_content)
    return article_content.replace(article_id, '')

def remove_duplicates(some_list):
    deduplicated_list = list(dict.fromkeys(some_list))
    return deduplicated_list

annotations = []
for line in lines:
    article_annotations = [annotation.strip().lower() for annotation in remove_id_from_article(line).split(",")]
    # print(article_annotations)
    annotations.extend(article_annotations)

deduplicated_list = remove_duplicates(annotations)
deduplicated_list.sort()
print(deduplicated_list)
print(len(annotations))
print(len(remove_duplicates(annotations)))
