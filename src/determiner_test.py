import itertools
import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from src.hardcoded_retriever import HardcodedRetriever
from src.tag_determiner import TagDeterminer
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor, LLMChainFilter
from langchain_openai import OpenAI, ChatOpenAI
from src.secrets import OPEN_API_KEY
import os
from src.tag_based_retriever import TagBasedRetriever

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


# input_path = "../documents/civilCodeSplitted/codex_tagged.json"
input_path = "../documents/civilCodeSplitted/articles_tagged.json"
tag_path = "../documents/tags.json"


retriever = TagBasedRetriever()
# llm = OpenAI(temperature=0)
# compressor = LLMChainFilter.from_llm(llm)
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, base_retriever=retriever
# )
#
# docs = compression_retriever.get_relevant_documents(
#     question
# )
# pretty_print_docs(docs)
question = "Jak może być wyrażone oświadczenie woli?"
retriever_prompt_template = """Given the following question:
{question}
And related articles:

<context>
{context}
</context>

Answer the question based on the articles provided articles. Answer in polish. In the answer refer to the corresponding article.
"""


retriever_prompt = ChatPromptTemplate.from_template(retriever_prompt_template)
model = ChatOpenAI(model_name="gpt-3.5-turbo")

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

retriever_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | retriever_prompt
    | model
    | StrOutputParser()
)

answer = retriever_chain.invoke(question)
print(answer)
# print(determined_tags)