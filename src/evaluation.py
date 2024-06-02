import json

import pandas as pd
from langchain_core.prompts import PromptTemplate
from src.agents.chat_gpt_4_answering_agent import ChatGPT4AnsweringAgent
from src.agents.complex_retrieval_agent import ComplexRetrievalAgent
from src.agents.tag_based_retrieval_agent import TagBasedRetrievalAgent
from src.agents.vector_database_retrieval_agent import VectorDatabaseRetrievalAgent
from src.agents.chat_gpt_3_5_answering_agent import ChatGPT35AnsweringAgent
from src.utils.utils import get_project_root

questions_path = get_project_root() / "documents" / "evaluation" / "closed_questions.csv"
# questions = pd.read_csv(questions_path, encoding="cp1250", delimiter=";")
questions_raw = pd.read_csv(questions_path, delimiter=",")

questions = questions_raw.to_dict(orient="records")


prompt_template = PromptTemplate.from_template(
"""There is a question: 
{question}
And three possible answers:
{answers}
Thought 1: Answer the questions and decide which of these three possible answers is correct
Thought 2: Choose the letter of corresponding answer from the
Thought 3: Respond in json format: with fields: answer, letter
""")

# agent = ChatGPT4AnsweringAgent()
# agent = ChatGPT35AnsweringAgent()
# agent = TagBasedRetrievalAgent()
# agent = VectorDatabaseRetrievalAgent()
agent = ComplexRetrievalAgent()
numerator = 0
results = []
for question_dict in questions:
    question = question_dict["question"]
    question_num = question_dict["numer pytania"]
    answers = question_dict["answers"]
    correct_answer = question_dict["correct_answer"]
    result = question_dict.copy()

    prompt = prompt_template.format(question=question, answers=answers)
    returned_answer = agent.answer(prompt)

    try:
        json_answer = json.loads(returned_answer)
        letter_chosen = json_answer["letter"]
        full_answer = json_answer["answer"]
        result["letter_chosen"] = letter_chosen
        result["full_answer"] = full_answer
    except:
        print("Answer is not in json format")
        pass
        letter_chosen = ""
    print(f"Pytanie {question_num}: {question}")
    print(f"Udzielona odpowiedź: {returned_answer}")
    print(f"Prawidłowa odpowiedź: {correct_answer}")

    result["raw_answer"] = returned_answer

    results.append(result)
    if letter_chosen == correct_answer or returned_answer == correct_answer + ")":
        numerator += 1

output_path = get_project_root() / "output" / "evaluation.json"
with open(output_path, "w") as f:
    json.dump(results, f)

print(f"Ilość dobrych odpowiedzi: {numerator}")
print(f"Jest to {numerator/len(questions)*100:.2f} % wszystkich odpowiedzi")

    # print(row['question'])
    # print(row["answers"])
    # print(row["correct_answer"])