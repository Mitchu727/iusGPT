from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from src.secrets import OPEN_API_KEY
import os

config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": OPEN_API_KEY,
        "base_url": "https://api.openai.com/v1",
    }
]


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
    user_proxy = UserProxyAgent(name="client", llm_config={"config_list": config_list})
    pro_agent = AssistantAgent(
        name="Analyzer",
        system_message="You have to analyze and answer given question in simple language and try to convince critic that you have right",
        llm_config={"config_list": config_list})
    contra_agent = AssistantAgent(
        name="Critic",
        system_message="Critic. You have to be critic to others ideas and find mistakes in their answers. You should especially check if other messages refer to law regulations",
        llm_config={"config_list": config_list})
    summarizer = AssistantAgent(
        name="Summarizer",
        system_message= "Try to summarize what others say"
    )

    prompt = """
        Dana jest następująca sprawa:
        Błażej ma 30 lat i nie jest ubezwłasnowolniony
        Odpowiedz czy posiada pełną zdolność do czynności prawnych.
    """


    groupchat = GroupChat(agents=[user_proxy, pro_agent, contra_agent], messages=[], max_round=20)
    manager = GroupChatManager(groupchat=groupchat, llm_config=config_list[0])
    user_proxy.initiate_chat(
        manager,
        message=prompt
    )
