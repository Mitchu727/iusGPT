from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
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

def load_articles_as_documents():
    path = "../documents/civilCodeSplitted/kodeks.json"
    with open(path, "r") as f:
        codex = json.load(f)
    documents = []
    for chapter in codex:
        for article in chapter["articles"]:
            document = Document(page_content=article)
            documents.append(document)
    return documents

if create_new_collection:
    # civil_code_path = "../documents/civilCodeTxtGenerated/kodeks.txt"
    # loader = TextLoader(civil_code_path)
    # documents = loader.load()
    # # FIXME ROOM FOR IMPROVEMENT - custom splitter
    # text_splitter = CharacterTextSplitter(
    #     separator="\n",
    #     chunk_size=1000,
    #     chunk_overlap=200,
    #     length_function=len,
    #     is_separator_regex=False,
    # )
    # docs = text_splitter.split_documents(documents)
    docs = load_articles_as_documents()
    print(len(docs))
    db = Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)

else:
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)

print("There are", db._collection.count(), "documents in the collection")

# query = "Czym jest gospodarstwo rolne?"
# docs = db.similarity_search(query, k=10)
# for doc in docs:
#     print(doc.page_content)

# rewrite_query_template = """Given the following question:
# {question}
#
# What are the concepts that should be checked in civil code to answer this question?
# """

# =====RETRIEVER=====
# retriever
retriever = db.as_retriever(search_kwargs={"k": 20})
retriever_prompt_template = """Here is the question:
{question}
And some articles that can be helpful to answer it:

<context>
{context}
</context>

Answer the given question on the base of the articles. In the answer refer to proper article.
"""

# template = """Use the following pieces of context to answer the question at the end. In an answer you should mention
# article from context.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.
# Use three sentences maximum and keep the answer as concise as possible.
#
# {context}
#
# Question: {question}
# """

retriever_prompt = ChatPromptTemplate.from_template(retriever_prompt_template)
model = ChatOpenAI()

retriever_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | retriever_prompt
    | model
    | StrOutputParser()
)
# =====PRO_AGENT=====

pro_agent_prompt_template = """Given the following articles from civil code:
{articles}

Answer given question: {question}. In the answer cite the proper article.
"""

pro_agent_prompt = ChatPromptTemplate.from_template(pro_agent_prompt_template)

pro_agent_chain = (
    # {"context": retriever_chain, "question": itemgetter("question")}
    pro_agent_prompt
    | model
    | StrOutputParser()
)

# =====CONTRA_AGENT=====

contra_agent_prompt_template = """There was a question: {question}
Some person provided following answer: {answer} based on following articles {articles}
You should find and write down any mistakes this person made.
"""

contra_agent_prompt = ChatPromptTemplate.from_template(contra_agent_prompt_template)

contra_agent_chain = (
    # {"context": retriever_chain, "question": itemgetter("question")}
    contra_agent_prompt
    | model
    | StrOutputParser()
)

# =====SUMMARY_AGENT=====

summary_agent_prompt_template = """There was a following question: {question} and the articles related to it {articles}.
One person answered it: {pro_response}
However some other person had some remarks: {contra_response}
Provide answer for given question based on those two opinions and related articles.
"""

summary_agent_prompt = ChatPromptTemplate.from_template(summary_agent_prompt_template)

summary_agent_chain = (
    # {"context": retriever_chain, "question": itemgetter("question")}
    summary_agent_prompt
    | model
    | StrOutputParser()
)


queries = [
    # "Czym jest gospodarstwo rolne?",
    # "Jaka jest definicja nieruchomości?",
    # "Komu przysługuje własność stanowiąca mienie państwowe?",
    # "Kim jest osoba ubezwłasnowolniona?",
    # "Co wchodzi w skład przedsiębiorstwa?",
    # "Jakie skutki wywołuje czynność prawna",
    # "Jak może być wyrażone oświadczenie woli?",
    # "Kiedy czynność prawna jest nieważna?",
    # "Czym jest prokura?",
    # "Kiedy kończy się termin oznaczony w dniach?",
    # "Co jest potrzebne do ważności czynności dokonanej przez ubezwłasnowolnionego?",
    # "Jaka forma pełnomocnictwa powinna być zawarta do zakupienia nieruchmości?",
    "Czy można żądać zadośćuczynienia/renty za pozbawienie wolności lub gwałt?"
]


experiments = []
for query in queries:
    answer = retriever_chain.invoke(query)
    # pro_response = pro_agent_chain.invoke({"articles": retrieved_documents, "question": query})
    # contra_response = contra_agent_chain.invoke({"question": query, "answer": pro_response, "articles": retrieved_documents})
    # summary_response = summary_agent_chain.invoke({"question": query, "articles": retrieved_documents, "pro_response": pro_response, "contra_response": contra_response})

    case = {}
    case["query"] = query
    case["retrieved_documents"] = answer
    # case["pro_response"] = pro_response
    # case["contra_response"] = contra_response
    # case["summary_response"] = summary_response
    print("<-PYTANIE->")
    print(query)
    print("<-ODPOWIEDŹ->")
    print(answer)
    experiments.append(case.copy())

with open('experiments.json', 'w') as f:
    json.dump(experiments, f)

from_json_to_xlsx('experiments.json', 'experiments.xlsx')