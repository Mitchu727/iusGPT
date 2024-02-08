from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from src.secrets import OPEN_API_KEY
import os
import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from config import config_list
docs_path = "C:\Praca magisterska\iusGPT\documents\simple"

law_assistant_prompt = """
    Assistant who has extra content retrieval power for regulations. When you get the case you should return the number 
    and the content of the law regulation. 
    """

law_assistant = RetrieveUserProxyAgent(
    name="Law Assistant",
    system_message=law_assistant_prompt,
    human_input_mode="NEVER",
    retrieve_config={
        "task": "code",
        "docs_path": docs_path,
        "collection_name": "law_simple",
        "get_or_create": True,
    }  # we don't want to execute code in this case.
)

def retrieve_content(message, n_results = 3):
    law_assistant.n_results = n_results  # Set the number of results to be retrieved.
    # Check if we need to update the context.
    update_context_case1, update_context_case2 = law_assistant._check_update_context(message)
    if (update_context_case1 or update_context_case2) and law_assistant.update_context:
        law_assistant.problem = message if not hasattr(law_assistant, "problem") else law_assistant.problem
        _, ret_msg = law_assistant._generate_retrieve_user_reply(message)
    else:
        ret_msg = law_assistant.generate_init_message(message, n_results=n_results)
    return ret_msg if ret_msg else message

llm_config = {
    "functions": [
        {
            "name": "retrieve_content",
            "description": "retrieve law regulations for given case.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Refined message that describes the case.",
                    }
                },
                "required": ["message"],
            },
        },
    ],
    "config_list": config_list
}

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
    user_proxy = UserProxyAgent(name="client", llm_config={"config_list": config_list})
    lawyer_agent = AssistantAgent(
        name="Lawyer",
        system_message="You are a lawyer. You have to analyze and answer given question in simple language. You can ask for regulations",
        llm_config=llm_config
    )

    simple_agent = AssistantAgent(
        name="Simple_man",
        system_message= "You are an ordinary man. You have to assess whether that what lawyer says is understandable",
        llm_config=llm_config
    )

    for agent in [lawyer_agent, simple_agent]:
        agent.register_function(
            function_map={
                "retrieve_content": retrieve_content,
            }
        )

    PROBLEM = """
        Stan faktyczny:
        Błażej ma 30 lat i nie jest ubezwłasnowolniony
        Pytanie:
        Odpowiedz czy posiada pełną zdolność do czynności prawnych.
    """

    groupchat = autogen.GroupChat(
        agents=[lawyer_agent, simple_agent],
        messages=[],
        max_round=12,
        allow_repeat_speaker=False,
    )

    manager_llm_config = llm_config.copy()
    manager_llm_config.pop("functions")
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=manager_llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    lawyer_agent.initiate_chat(
        manager,
        message=PROBLEM,
    )
