from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from src.flows.flow_interface import FlowInterface

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever


class SimpleRagFlow(FlowInterface):

    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0, k=10):
        self.model = model
        self.temperature = temperature
        self.k = k

        docs = load_articles_as_documents()
        retriever = create_chroma_retriever(docs, k)
        retriever_tool = create_retriever_tool(
            retriever,
            "civil_code",
            "Search for information in polish civil code.",
        )
        tools = [retriever_tool]
        llm = ChatOpenAI(model=model, temperature=temperature)

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=[],
                    template=self.system_prompt
                )
            ),
            MessagesPlaceholder(variable_name='chat_history', optional=True),
            HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
            MessagesPlaceholder(variable_name='agent_scratchpad')
        ])
        agent = create_tool_calling_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, stream_runnable=False, verbose=True)


    def answer_evaluation_question(self, question_dict):
        formatted_question = self.format_question(question_dict)
        return self.agent_executor.invoke({"input": formatted_question})["output"]


    def get_flow_name(self):
        return f"simple_rag_{self.model}_{self.temperature}"

    def get_flow_parameters(self):
        return {
            'model': self.model,
            'temperature': self.temperature,
            'k': self.k,
            'system_prompt': self.system_prompt,
            'evaluation_prompt_template': self.evaluation_prompt_template,
            'vectorstore': 'chroma'
        }
