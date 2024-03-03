from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
import os
from src.secrets import OPEN_API_KEY
import json
from utils.formatter import from_json_to_xlsx

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

model_name = "sdadas/mmlw-roberta-base"
embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
# model_name = "all-MiniLM-L6-v2"
persist_directory = "../build"
create_new_collection = True

if create_new_collection:
    civil_code_path = "../documents/civilCodeTxtGenerated/kodeks.txt"
    loader = TextLoader(civil_code_path)
    documents = loader.load()
    # FIXME ROOM FOR IMPROVEMENT - custom splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    docs = text_splitter.split_documents(documents)
    db = Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)

else:
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)

print("There are", db._collection.count(), "documents in the collection")

query = "Czym jest gospodarstwo rolne?"
docs = db.similarity_search(query, k=10)
for doc in docs:
    print(doc.page_content)

# retriever
retriever = db.as_retriever()

# template = """Answer the question based only on the following context:
# {context}
#
#
# Decide which articles from context are relevant to the following question:
# {context}
#
# Question: {question}
#
# In the answer you should only type the given question and articles related to it.
#
# """

template = """Use the following pieces of context to answer the question at the end. In an answer you should mention 
article from context. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.

{context}

Question: {question}
"""

queries = [
    "Czym jest gospodarstwo rolne?",
    "Jaka jest definicja nieruchomości?",
    "Komu przysługuje własność stanowiąca mienie państwowe?",
    "Kim jest osoba ubezwłasnowolniona?",
    "Co wchodzi w skład przedsiębiorstwa?",
    "Jakie skutki wywołuje czynność prawna",
    "Jak może być wyrażone oświadczenie woli?",
    "Kiedy czynność prawna jest nieważna",
    "Czym jest prokura?",
    "Kiedy kończy się termin oznaczony w dniach?"
]

prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
experiments = []
for query in queries:
    response = chain.invoke(query)
    case = {}
    case["query"] = query
    case["answer"] = response
    print("<-PYTANIE->")
    print(query)
    print("<-ODPOWIEDŹ->")
    print(response)
    experiments.append(case.copy())

with open('experiments.json', 'w') as f:
    json.dump(experiments, f)

from_json_to_xlsx('experiments.json', 'experiments.xlsx')