from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
import src.secrets


class ReactRagFlow:
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
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
        print(prompt)

        prompt.template = """
            You are a helpful assistant specializing in Polish civil law. You will receive questions from
            an exam, each consisting of a question or an incomplete sentence followed by three possible answers labeled
            a, b, and c.
    
            Your task is to:
            1. Choose the correct answer.
            2. Provide a detailed explanation for your choice.
            3. Refer to the relevant article(s) in the Polish Civil Code.
    
            Please ensure your answers are precise and informative.
    
            You have access to the following tools:
    
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

        agent = create_react_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

        self.human_prompt_template = """
            Question: {question}

            a) {answer_a}
            b) {answer_b}
            c) {answer_c}

            Please choose the correct answer (a, b, or c), provide an explanation, and refer to the relevant article(s) 
            in the Polish Civil Code."""

    def format_question(self, question_dict):
        return self.human_prompt_template.format(
            index=question_dict["index"],
            question=question_dict["question"],
            answer_a=question_dict["a"],
            answer_b=question_dict["b"],
            answer_c=question_dict["c"]
        )

    def answer_evaluation_question(self, question_dict):
        formatted_question = self.format_question(question_dict)
        return self.agent_executor.invoke({"input": formatted_question})["output"]


if __name__ == "__main__":
    question_dict = {
        "index": 30,
        "question": "Zgodnie z Kodeksem cywilnym, ograniczoną zdolność do czynności prawnych mają:",
        "a": "osoby ubezwłasnowolnione całkowicie",
        "b": "małoletni, którzy ukończyli lat dziesięć, oraz osoby ubezwłasnowolnione całkowicie",
        "c": "małoletni, którzy ukończyli lat trzynaście, jeżeli nie zostali ubezwłasnowolnieni całkowicie, oraz osoby ubezwłasnowolnione częściowo"
    }
    flow = ReactRagFlow("gpt-3.5-turbo-0125", 0)
    print(flow.answer_evaluation_question(question_dict))