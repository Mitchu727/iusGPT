from src.agents.vector_database_retrieval_agent import VectorDatabaseRetrievalAgent
from src.agents.chat_gpt_4_answering_agent import ChatGPT4AnsweringAgent
from src.agents.tag_based_retrieval_agent import TagBasedRetrievalAgent
import pandas as pd

questions_path = "../documents/evaluation/open_questions.csv"
vector_agent = VectorDatabaseRetrievalAgent()
question = "Jaka jest definicja nieruchmości?"
#
# vector_answer = vector_agent.answer(question)
# print(vector_answer)
#
chat_4_agent = ChatGPT4AnsweringAgent()
chat_4_answer = chat_4_agent.answer(question)
print(chat_4_answer)
#
# tag_based_agent = TagBasedRetrievalAgent()
# tag_answer = tag_based_agent.answer(question)
# print(tag_answer)

# questions = pd.read_csv(questions_path, encoding="utf-8", delimiter=";")
# print(questions)
# questions["vector_response"] = questions["Pytanie"].apply(lambda question: vector_agent.answer(question))
# questions["tag_response"] = questions["Pytanie"].apply(lambda question: tag_based_agent.answer(question))
# questions["chat_gpt_4_response"] = questions["Pytanie"].apply(lambda question: chat_4_agent.answer(question))
# questions.to_excel("evaluation.xlsx")