from src.agents.vector_database_retrieval_agent import VectorDatabaseRetrievalAgent
from src.agents.chat_gpt_4_answering_agent import ChatGPT4AnsweringAgent
from src.agents.tag_based_retrieval_agent import TagBasedRetrievalAgent


question = "Jaka jest definicja nieruchmości?"

vector_agent = VectorDatabaseRetrievalAgent()
vector_answer = vector_agent.answer(question)
print(vector_answer)

# chat_4_agent = ChatGPT4AnsweringAgent()
# chat_4_answer = chat_4_agent.answer(question)
# print(chat_4_answer)

tag_based_agent = TagBasedRetrievalAgent()
tag_answer = tag_based_agent.answer(question)
print(tag_answer)