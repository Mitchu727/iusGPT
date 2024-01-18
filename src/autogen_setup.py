from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, oai
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
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample.json
    # config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    assistant = AssistantAgent(name="assistant", llm_config={"config_list": config_list})
    user_proxy = UserProxyAgent(name="user_proxy", llm_config={"config_list": config_list})
    user_proxy.initiate_chat(
        assistant,
        message="""Hello, today you are my data analyst assistant and you should help me visualize data, make predictions, and explain your thinking.""",
    )
    response = oai.Completion.create(
        config_list=config_list,
        prompt="Hi",
    )
    response = oai.ChatCompletion.create(
        config_list=config_list,
        messages=[{"role": "user", "content": "Hi"}]
    )
    print(response)
    # This initiates an automated chat between the two agents to solve the task