from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI

from src.flows.flow_interface import FlowInterface
from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
import src.secrets
from src.utils.utils import get_example_question


class ReactRagFlow(FlowInterface):
    react_prompt_template = """
            {system_prompt}
    
            However only the final answer should be in polish, you can use english in other cases.
            While performing this task you have access to the following tools:
    
            {tools}
    
            Use the following format:
    
            Question: the input question you must answer
            Thought: you should always think about what to do, if your previous action did not meet expectations you can try with different parameters
            Action: the action to take, should be one of [{tool_names}] without parameters
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question.
    
            Begin!
    
            Question: {input}
            Thought:{agent_scratchpad}
            """

    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        self.model = model
        self.temperature = temperature

        docs = load_articles_as_documents()
        retriever = create_chroma_retriever(docs, 10)
        retriever_tool = create_retriever_tool(
            retriever,
            "civil_code",
            "Search for information in polish civil code.",
        )
        tools = [retriever_tool]
        llm = ChatOpenAI(model=model, temperature=temperature)

        prompt = hub.pull("hwchase17/react")
        prompt.template = self.react_prompt_template

        agent = create_react_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


    def answer_evaluation_question(self, question_dict):
        formatted_question = self.format_question(question_dict)
        return self.agent_executor.invoke(
            {
                "input": formatted_question,
                "system_prompt": self.system_prompt
            }
        )["output"]

    def get_flow_name(self):
        return f"react_{self.model}_{self.temperature}_chroma"

    def get_flow_parameters(self):
        return {
            'model': self.model,
            'temperature': self.temperature,
            'system_prompt': self.system_prompt,
            'evaluation_prompt_template': self.evaluation_prompt_template,
            'react_prompt_template': self.react_prompt_template,
            'vectorstore': 'chroma'
        }


if __name__ == "__main__":
    question = get_example_question()
    flow = ReactRagFlow("gpt-3.5-turbo-0125", 0)
    print(flow.answer_evaluation_question(question))
