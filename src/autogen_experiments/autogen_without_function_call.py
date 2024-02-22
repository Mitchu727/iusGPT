from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from src.secrets import OPEN_API_KEY
import os
import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from utils import config_list, termination_msg, llm_config, PROBLEM
from src.secrets import HUGGING_FACE_API_KEY
from chromadb.utils import embedding_functions

docs_path = "C:\Praca magisterska\iusGPT\documents\simple"


huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=HUGGING_FACE_API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

law_assistant_prompt = """
    Assistant who has extra content retrieval power for regulations. 
    You should respond only with the full text of the regulation that is helpful to answer the question.
    """

assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message=law_assistant_prompt,
    llm_config=config_list[0],
)

law_assistant = RetrieveUserProxyAgent(
    name="law_assistant",
    retrieve_config={
        "task": "qa",
        "docs_path": docs_path,
        "embedding_function": huggingface_ef,
    },
)



# law_assistant = RetrieveUserProxyAgent(
#     name="Law_Assistant",
#     system_message=law_assistant_prompt,
#     human_input_mode="NEVER",
#     retrieve_config={
#         "task": "qa",
#         "docs_path": docs_path,
#         "collection_name": "law_simple",
#         "get_or_create": True,
#     }  # we don't want to execute code in this case.
# )

client = autogen.UserProxyAgent(
    name="Client",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="The client who ask questions and needs answers.",
    code_execution_config=False,  # we don't want to execute code in this case.
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)

lawyer_agent = AssistantAgent(
    name="Lawyer",
    system_message="You are a lawyer. You have to analyze and answer given question in simple language. You can ask for regulations",
    llm_config=llm_config
)

simple_agent = AssistantAgent(
    name="Simple_man",
    system_message="You are a simple man. You have to assess whether that what lawyer says is understandable",
    llm_config=llm_config
)

if __name__ == "__main__":
    law_assistant.reset()
    lawyer_agent.reset()
    simple_agent.reset()

    groupchat = autogen.GroupChat(
        agents=[law_assistant, lawyer_agent, simple_agent], messages=[], max_round=12, speaker_selection_method="round_robin"
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss_aid as this is the user proxy agent.
    law_assistant.initiate_chat(
        manager,
        problem=PROBLEM,
        n_results=10,
    )
