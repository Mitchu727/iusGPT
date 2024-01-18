from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from src.secrets import OPEN_API_KEY
import os
from cases_loader import CasesLoader

config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": OPEN_API_KEY,
        "base_url": "https://api.openai.com/v1",
    }
]


def format_case_and_question(case, question):
    return f"{case}\n\n{question}"


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
    user_proxy = UserProxyAgent(name="client", llm_config={"config_list": config_list})
    pro_agent = AssistantAgent(
        name="pro_agent",
        system_message="Zostanie Ci przedstawiona sprawa prawna i pytanie do niej. Odpowiedz na to pytanie.",
        llm_config={"config_list": config_list})
    contra_agent = AssistantAgent(
        name="contra_agent",
        system_message="Przedstaw przeciwne zdanie",
        llm_config={"config_list": config_list})

    cases_loader = CasesLoader()
    # assistant = AssistantAgent(name="opponent", llm_config={"config_list": config_list})

    case = cases_loader.load_case(1)
    question = cases_loader.load_questions(1)[0]
    message = format_case_and_question(case, question)

    groupchat = GroupChat(agents=[user_proxy, pro_agent, contra_agent], messages=[], max_round=20)
    manager = GroupChatManager(groupchat=groupchat, llm_config=config_list[0])
    user_proxy.initiate_chat(
        manager,
        message=message
    )
