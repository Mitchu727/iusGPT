import json

from src.flows.react_rag_flow import ReactRagFlow
from src.flows.simple_rag_flow import SimpleRagFlow
from src.utils.utils import get_project_root
from src.flows.simple_flow import SimpleFlow
from src.flows.judge import Judge

dataset_path = get_project_root() / "documents" / "evaluation" / "civil_law_exam"
questions_path = dataset_path / "questions.json"
answers_path = dataset_path / "answers.json"

with open(questions_path, "r") as f:
    questions = json.load(f)

with open(answers_path, "r") as f:
    answers = json.load(f)

# evaluated_flow = SimpleFlow("gpt-4o", 0)  # 45, 46
# evaluated_flow = SimpleFlow("gpt-4", 0)  # 48, 17
# evaluated_flow = SimpleFlow("gpt-4o-mini", 0)  # 39, 20
# evaluated_flow = SimpleFlow("gpt-3.5-turbo-0125", 0)  # 25, 7
# evaluated_flow = SimpleRagFlow("gpt-3.5-turbo-0125", 0)  # 45, 47
# evaluated_flow = SimpleRagFlow("gpt-4o", 0)  # 59, 63
# evaluated_flow = SimpleRagFlow("gpt-4o-mini", 0)  # 56, 52
# evaluated_flow = ReactRagFlow("gpt-4o-mini", 0)  # 49, 55
evaluated_flow = ReactRagFlow("gpt-3.5-turbo-0125", 0)  # 44, 41
judge = Judge("gpt-3.5-turbo-0125", 0)

# TODO
#  - Knowledge graph -> to ładnie wyląda
#  - kartkowanie -> to jest oryginalne i tego chciałby promotor
#  - strojenie promptów do react'a + dodanie narzędzi -> rozwinięcie react'a które dałoby się obronić
#  - lepsze logowanie -> must have gdy będę miał chwilę
#  - więcej pytań -> nice to have gdy będę miał chwilę



correct_answer_counter = 0
correct_article_counter = 0
# for i in range(10):
for i in range(len(questions)):
    question = questions[i]
    answer = answers[i]
    evaluated_answer = evaluated_flow.answer_evaluation_question(question)
    evaluation_result = judge.assess_evaluation_question(question,  answer, evaluated_answer)

    print(evaluated_answer)
    print(evaluation_result)

    result = json.loads(evaluation_result)
    if result["answer_is_correct"] is True:
        correct_answer_counter += 1
    if result["article_is_correct"] is True:
        correct_article_counter += 1

print(correct_answer_counter)
print(correct_article_counter)
