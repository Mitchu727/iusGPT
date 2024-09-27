import os

import regex as re
import json

from src.utils.utils import get_project_root, extract_id_from_article_content

list_of_directories = [directory for directory in os.listdir() if directory[-3:] != ".py"]
for dir_name in list_of_directories:
    print(dir_name)
    dir_path = get_project_root() / "documents" / "legal_acts" / "batch" / dir_name
    json_file_path = dir_path / "source.json"
    txt_file_path = dir_path / "source.txt"
    lookup_file_path = dir_path / "lookup.txt"

    with open(txt_file_path, "r", encoding="UTF-8") as f:
        text = f.read()

    text = re.sub(r"((\n|.)*?)(KSIĘGA|CZĘŚĆ|DZIAŁ|TYTUŁ)", r"\3", text, 1)
    text = re.sub(r"( |\n)*©Kancelaria Sejmu(.|\n)*?[0-9]{4}-[0-9]{2}-[0-9]{2}( |)*", "", text)
    text = re.sub(r"\n *\n(\S.*\n)*.*(Niniejsza ustawa|Utracił moc|wyroku \n*Trybunału \n*Konstytucyjnego|Zmiany tekstu jednolitego|Zmiany wymienionego rozporządzenia|Zmiana wymienionego rozporządzenia| Zmiany wymienionej ustawy).*\n(.*\n)*?(\S.*\n)*", "", text)
    text = re.sub(r'\nArt. [0-9]*\. \(uchylony\)', '', text)
    text = re.sub(r'\nArt. [0-9|–]*\. \(uchylone\)', '', text)
    text = re.sub(r'\nArt. [0-9|–]*\. \(pominięte\)', '', text)
    text = re.sub(r'\nArt. [0-9]*–[0-9]*\..*', '', text)

    text = text.replace("\n", "")
    text = text.replace("Art.", "\nArt.")
    text = re.sub(r'(KSIĘGA [^\n]+) *\n', r'\n', text)
    text = re.sub(r'(TYTUŁ [^\n]+) *\n', r'\n', text)
    text = re.sub(r'(DZIAŁ [^\n]+) *\n', r'\n', text)
    text = re.sub(r'(CZĘŚĆ [^\n]+) *\n', r'\n', text)
    text = re.sub(r'(Rozdział [^\n]+) *\n', r'\n', text)
    text = re.sub(r'(Oddział [^\n]+) *\n', r'\n', text)
    # text = re.sub(r'\n(Art\. [^\.]+stosuje się odpowiednio)', r'\1', text)
    text = re.sub(r'\n(((Art\.|art\.)[^\.]*)+[^\.]*stosuje się odpowiednio\.)', r'\1', text)
    text = re.sub(r'\n(((Art\.|art\.)[^\.]*)+[^\.]*stosuje się\.)', r'\1', text)
    text = text[1:]

    with open(lookup_file_path, "w+", encoding="UTF-8") as f:
        f.write(text)

    articles = []
    for element in text.split("\n"):
        element = element.strip()
        article = {
            "id": extract_id_from_article_content(element),
            "content": element
        }
        articles.append(article)

    with open(json_file_path, "w+") as f:
        json.dump(articles, f)
    # \n *\n[0-9]+\)(.\n*)*?(Utracił moc|wyroku Trybunału Konstytucyjnego|Zmiany tekstu jednolitego|Zmiany wymienionego rozporządzenia)(.|\n)*?\n *\n
    #
    # book = ""
    # title = ""
    # section = ""
    # chapter = ""
    # articles = []
    # for element in text.split("\n\n"):
    #     if "KSIĘGA" in element:
    #         book = element
    #         title = ""
    #         section = ""
    #         chapter = ""
    #     if "TYTUŁ" in element:
    #         title = element
    #         section = ""
    #         chapter = ""
    #     if "DZIAŁ" in element:
    #         section = element
    #         chapter = ""
    #     if "Rozdział" in element:
    #         chapter = element
    #     if element.startswith("Art."):
    #         article = {
    #             "id": extract_id_from_article(element),
    #             "book": book,
    #             "title": title,
    #             "section": section,
    #             "chapter": chapter,
    #             "content": element
    #         }
    #         articles.append(article)
    #
    # with open(json_file_path, "w+") as f:
    #     json.dump(articles, f)
