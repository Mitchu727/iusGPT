import os

import fitz
import regex as re
import json

from src.utils.utils import get_project_root, extract_id_from_article_content, get_legal_acts_list_from_directories
import logging


def extract_legal_acts_from_pdf_to_txt(list_of_directories):
    for dir_path in list_of_directories:
        logging.info(f"Extracting legal act from pdf to txt: {dir_path}")
        # dir_path = get_project_root() / "documents" / "legal_acts" / "batch" / dir_path
        pdf_file_path = dir_path / "source.pdf"
        txt_file_path = dir_path / "source.txt"
        doc = fitz.open(pdf_file_path)
        text_pages = []
        for page in doc:
            text = page.get_text()
            text_pages.append(text)

        with open(txt_file_path,"w", encoding="UTF-8") as f:
            f.write("\n".join(text_pages))


def extract_legal_acts_from_txt_to_json(list_of_directories):
    for dir_path in list_of_directories:
        logging.info(f"Extracting legal act from txt to json: {dir_path}")
        json_file_path = dir_path / "source.json"
        txt_file_path = dir_path / "source.txt"
        lookup_file_path = dir_path / "lookup.txt"

        with open(txt_file_path, "r", encoding="UTF-8") as f:
            text = f.read()

        text = re.sub(r"((\n|.)*?)(KSIĘGA|CZĘŚĆ|DZIAŁ|TYTUŁ|Rozdział|Art)", r"\3", text, 1)
        text = re.sub(r"( |\n)*©Kancelaria Sejmu(.|\n)*?[0-9]{4}-[0-9]{2}-[0-9]{2}( |)*", "", text)
        text = re.sub(r"\n *\n(\S.*\n)*.*(Niniejsza ustawa|Utracił moc|wyroku \n*Trybunału \n*Konstytucyjnego|Zmiany tekstu jednolitego|Zmiany wymienionego rozporządzenia|Zmiana wymienionego rozporządzenia| Zmiany wymienionej ustawy).*\n(.*\n)*?(\S.*\n)*", "", text)
        text = re.sub(r'\nArt. [0-9]*\. \(uchylony\)', '', text)
        text = re.sub(r'\nArt. [0-9|–]*\. \(uchylone\)', '', text)
        text = re.sub(r'\nArt. [0-9|–|a]*\. \(pominięte\)', '', text)
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


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    list_of_directories = get_legal_acts_list_from_directories()
    extract_legal_acts_from_pdf_to_txt(list_of_directories)
    extract_legal_acts_from_txt_to_json(list_of_directories)