import json

from src.evaluation_logger import EvaluationLogger
from src.flows.concept_flow.concept_flow import ConceptFlow
from src.flows.simple_rag_flow import SimpleRagFlow
from src.utils.utils import get_project_root, format_question, format_answer
from src.flows.judge import Judge

dataset_path = get_project_root() / "documents" / "evaluation" / "civil_law_exam"
questions_path = dataset_path / "questions.json"
answers_path = dataset_path / "answers.json"
from langchain_community.callbacks import get_openai_callback

with open(questions_path, "r") as f:
    questions = json.load(f)

with open(answers_path, "r") as f:
    answers = json.load(f)

# evaluated_flow = SimpleFlow("gpt-4o-mini", 0)  # 46, 38
# evaluated_flow = SimpleFlow("gpt-4o", 0)  # 83, 97
# evaluated_flow = SimpleFlow("gpt-3.5-turbo-0125", 0)  # 25, 7
# evaluated_flow = SimpleRagFlow("gpt-3.5-turbo-0125", 0, 75)  # 45, 47
# evaluated_flow = SimpleRagFlow("gpt-4o", 0)  # 59, 63
# evaluated_flow = SimpleRagFlow("gpt-4o-mini", 0, 100)  # 56, 52  # 116, 114
# evaluated_flow = ReactRagFlow("gpt-4o-mini", 0)  # 49, 55
# evaluated_flow = ReactRagFlow("gpt-3.5-turbo-0125", 0)  # 44, 41
evaluated_flow = ConceptFlow(
    chapter_selector_model="gpt-4o-mini",
    article_selector_model="gpt-4o-mini",
    answering_agent_model="gpt-4o-mini",
)

judge = Judge("gpt-4o-mini", 0)

# TODO
#  - Knowledge graph -> to ładnie wyląda
#  - kartkowanie -> to jest oryginalne i tego chciałby promotor
#  - strojenie promptów do react'a + dodanie narzędzi -> rozwinięcie react'a które dałoby się obronić


logger = EvaluationLogger(evaluated_flow)

correct_answer_count = 0
correct_article_count = 0
for i in range(5):
# for i in range(len(questions)):
# for i in [92, 102, 113]:
    question_dict = questions[i]
    answer_dict = answers[i]

    print("==========PYTANIE==========")
    print(format_question(question_dict))
    print("==========PRAWIDŁOWA ODPOWIEDŹ==========")
    print(format_answer(answer_dict))

    print("==========KOSZTY==========")
    with get_openai_callback() as cb:
        evaluated_answer = evaluated_flow.answer_evaluation_question(question_dict)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")
    evaluation_result = judge.assess_evaluation_question(question_dict, answer_dict, evaluated_answer)

    print("==========ODPOWIEDŹ==========")
    print(evaluated_answer)
    print("==========KLASYFIKACJA==========")
    print(evaluation_result)

    try:
        result = json.loads(evaluation_result)
    except:
        result = {
            "answer_is_correct": False,
            "article_is_correct": False
        }
    if result["answer_is_correct"] is True:
        correct_answer_count += 1
    if result["article_is_correct"] is True:
        correct_article_count += 1
    logger.log_evaluation_result(question_dict, answer_dict, evaluated_answer, result)

logger.save_end_results(correct_answer_count, correct_article_count, len(questions))

print(correct_answer_count)
print(correct_article_count)
print(len(questions))

# TODO
# refactor
# k-means na embeddingach