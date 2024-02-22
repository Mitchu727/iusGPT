# BASED ON https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat_RAG.ipynb

import autogen
from utils import config_list, termination_msg
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb
from autogen import AssistantAgent


llm_config = {
    "config_list": config_list,
}

# autogen.ChatCompletion.start_logging()

docs_path = "C:\Praca magisterska\iusGPT\documents\simple"

law_assistant_prompt = """
    Assistant who has extra content retrieval power for regulations. When you get the case you should return the number 
    and the content of the law regulation. 
    """

boss = autogen.UserProxyAgent(
    name="Boss",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="The boss who ask questions and give tasks.",
    code_execution_config=False,  # we don't want to execute code in this case.
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)

law_assistant = RetrieveUserProxyAgent(
    name="Law Assistant",
    system_message=law_assistant_prompt,
    human_input_mode="NEVER",
    retrieve_config={
        "docs_path": docs_path,
        "collection_name": "law_simple",
        "get_or_create": True,
    }  # we don't want to execute code in this case.
)

lawyer_agent_prompt = """
You are a lawyer. You have to analyze and answer given question in simple language. 
When you respond you should give proper number of law regulation You can ask for regulations.
"""
lawyer_agent = autogen.AssistantAgent(
    name="Lawyer",
    is_termination_msg=termination_msg,
    system_message=lawyer_agent_prompt,
    llm_config=llm_config,
)

PROBLEM = """
        Stan faktyczny:
        Błażej ma 30 lat i nie jest ubezwłasnowolniony
        Pytanie:
        Odpowiedz czy posiada pełną zdolność do czynności prawnych.
    """

def _reset_agents():
    boss.reset()
    law_assistant.reset()
    lawyer_agent.reset()

def call_rag_chat():
    _reset_agents()

    # In this case, we will have multiple user proxy agents and we don't initiate the chat
    # with RAG user proxy agent.
    # In order to use RAG user proxy agent, we need to wrap RAG agents in a function and call
    # it from other agents.
    def retrieve_content(message, n_results=3):
        law_assistant.n_results = n_results  # Set the number of results to be retrieved.
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = law_assistant._check_update_context(message)
        if (update_context_case1 or update_context_case2) and law_assistant.update_context:
            law_assistant.problem = message if not hasattr(law_assistant, "problem") else law_assistant.problem
            _, ret_msg = law_assistant._generate_retrieve_user_reply(message)
        else:
            ret_msg = law_assistant.generate_init_message(message, n_results=n_results)
        return ret_msg if ret_msg else message

    law_assistant.human_input_mode = "NEVER"  # Disable human input for boss_aid since it only retrieves content.

    llm_config = {
        "functions": [
            {
                "name": "retrieve_content",
                "description": "Retrieve law regulations for given case.",
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
        "config_list": config_list,
    }

    for agent in [lawyer_agent]:
        # update llm_config for assistant agents.
        agent.llm_config.update(llm_config)

    for agent in [boss, lawyer_agent]:
        # register functions for all agents.
        agent.register_function(
            function_map={
                "retrieve_content": retrieve_content,
            }
        )

    groupchat = autogen.GroupChat(
        agents=[boss, lawyer_agent],
        messages=[],
        max_round=12,
        speaker_selection_method="random",
        allow_repeat_speaker=False,
    )

    manager_llm_config = llm_config.copy()
    manager_llm_config.pop("functions")
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=manager_llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=PROBLEM,
    )

if __name__ == "__main__":
    call_rag_chat()