import json
import os
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


from src.utils.utils import get_project_root, extract_id_from_article_content
import src.secret

civil_articles_path = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"
output_file_path = "chapters_annotated.txt"

class ChapterAnnotator:
    system_prompt = """
        Context:
        You will receive a specific excerpt from the civil code, which includes the article ID, along with tags that describe the legal concepts, institutions, and relationships that the article addresses.
        
        Task:
        Your task is to create a comprehensive description of this excerpt. This description should encapsulate all the concepts, institutions, and relationships mentioned, even if they appear only briefly or infrequently. The objective is to ensure that anyone searching for information related to the content of this article will be able to identify it as relevant and applicable based on your description.
        """


    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        self.model = model
        self.temperature = temperature

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{chapter}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def annotate_chapter(self, article_content):
        return self.chain.invoke({"chapter": article_content})


if __name__ == '__main__':
    chapter_ids = [
        "KSIĘGA PIERWSZA CZĘŚĆ OGÓLNA",
        "KSIĘGA DRUGA WŁASNOŚĆ I INNE PRAWA RZECZOWE",
        "KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_OGÓLNA",
        "KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_SZCZEGÓŁOWA_CZĘŚĆ_PIERWSZA",
        "KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_SZCZEGÓŁOWA_CZĘŚĆ_DRUGA",
        "KSIĘGA CZWARTA SPADKI"
    ]
    chapter_files = [file for file in os.listdir() if file.startswith('chapter_') and file.endswith(".txt")]
    annotator = ChapterAnnotator()
    chapter_annotations = []
    for index, chapter_file in enumerate(chapter_files):
        print(chapter_ids[index])
        with open(chapter_file, 'r') as f:
            content = f.read()
        annotation = annotator.annotate_chapter(content)
        annotation_with_id = f"{chapter_ids[index]}\n{annotation}"
        chapter_annotations.append(annotation_with_id)

    text = "\n\n".join(chapter_annotations)

    with open(output_file_path, "w") as f:
        f.write(text)
