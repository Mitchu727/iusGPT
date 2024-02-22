import autogen

from src.cases_loader import CasesLoader
from utils import config_list, PROBLEM
from src.secrets import OPEN_API_KEY, HUGGING_FACE_API_KEY
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from chromadb.utils import embedding_functions

huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=HUGGING_FACE_API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="""
    Assistant who has extra content retrieval power for regulations. 
    You should respond only with the full text of the regulation that is helpful to answer the question.
    """,
    llm_config=config_list[0],
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",
        "docs_path": "C:\Praca magisterska\iusGPT\documents\simple",
        "embedding_function": huggingface_ef,
    },
)

if __name__ == "__main__":
    assistant.reset()

    # cases_loader = CasesLoader()
    # case = cases_loader.load_case(3)
    #
    # question = cases_loader.load_questions(3)[0]



    ragproxyagent.initiate_chat(assistant, problem=PROBLEM)
