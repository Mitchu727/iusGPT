import json

from src.evaluation_logger import EvaluationLogger
from src.flows.concept_flow.concept_flow import ConceptFlow
from src.flows.multi_agent_flow import MultiAgentFlow
from src.flows.multi_agent_flow_advanced_rag import MultiAgentFlowAdvancedRag
from src.flows.multi_agent_flow_simple_rag import MultiAgentFlowSimpleRag
from src.flows.simple_flow import SimpleFlow
from src.flows.simple_rag_flow import SimpleRagFlow
from src.flows.simple_rag_search_flow import SimpleRagSearchFlow
from src.utils.utils import get_project_root, format_question, format_answer, remove_superscripts
from src.flows.judge import Judge
from langchain_community.callbacks import get_openai_callback
import random


def load_questions_for_codes(code_list):
    questions = []
    answers = []
    for code in code_list:
        dataset_path = get_project_root() / "documents" / "evaluation" / "extracted" / code
        questions_path = dataset_path / "questions.json"
        answers_path = dataset_path / "answers.json"
        with open(questions_path, "r") as f:
            code_questions = json.load(f)
        questions.extend(code_questions)
        with open(answers_path, "r") as f:
            code_answers = json.load(f)
        answers.extend(code_answers)
    return questions, answers


def load_questions_from_directory(directory_path):
    questions_path = directory_path / "questions.json"
    answers_path = directory_path / "answers.json"
    with open(questions_path, "r") as f:
        questions = json.load(f)
    with open(answers_path, "r") as f:
        answers = json.load(f)
    return questions, answers


# dataset_path = get_project_root() / "documents" / "evaluation" / "penal_code_questions"
questions, answers = load_questions_for_codes(["civil_code"])
# questions, answers = load_questions_from_directory(get_project_root() / "documents" / "evaluation" / "original" / "egzamin_wstepny_adwokacki_radcowski_2024")

# evaluated_flow = SimpleFlow("gpt-3.5-turbo-0125", 0)  # 77, 26
# evaluated_flow = SimpleFlow("gpt-4o-mini", 0)  # 101, 58
# evaluated_flow = SimpleFlow("gpt-4", 0)  # 115, 53
# evaluated_flow = SimpleFlow("gpt-4o", 0)

# evaluated_flow = SimpleRagSearchFlow("gpt-3.5-turbo-0125", 0, 50)  # 112, 126
# evaluated_flow = SimpleRagSearchFlow("gpt-4o-mini", 0, 50) # 128, 139
#
# evaluated_flow = SimpleRagFlow("gpt-3.5-turbo-0125", 0) #101, 116
# evaluated_flow = SimpleRagFlow("gpt-4o-mini", 0) # 130 128
# evaluated_flow = MultiAgentFlowSimpleRag("gpt-4o-mini", 0, 20)
evaluated_flow = MultiAgentFlowAdvancedRag("gpt-4o-mini", 0, 20)

judge = Judge("gpt-4o-mini", 0)

logger = EvaluationLogger(evaluated_flow)
context_used = 0
correct_answer_count = 0
correct_context_count = 0
joint_score = 0
questions_num = 0

# # list of hard questions
# hard_questions_list = [5, 9, 15, 16, 29, 35, 48, 82, 102, 108, 125, 126, 128]
# questions = [questions[i] for i in hard_questions_list]
# answers = [answers[i] for i in hard_questions_list]

for i in range(len(questions)):
    question_dict = questions[i]
    answer_dict = answers[i]

    questions_num += 1

    try:
        with get_openai_callback() as cb:
            evaluated_answer = remove_superscripts(evaluated_flow.answer_evaluation_question(question_dict))
            print("==========KOSZTY==========")
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            context_used += cb.total_tokens
        evaluation_result = judge.assess_evaluation_question(question_dict, answer_dict, evaluated_answer)
        result = json.loads(evaluation_result)
    except Exception as e:
        print(e)
        result = {
            "chosen_answer": "",
            "referred_articles": []
        }

    print(f"==========PYTANIE {questions_num}==========")
    print(format_question(question_dict))
    print("==========PRAWIDŁOWA ODPOWIEDŹ==========")
    print(format_answer(answer_dict))
    print("==========ODPOWIEDŹ==========")
    print(evaluated_answer)
    print("==========KLASYFIKACJA==========")
    print(result)

    answer_is_correct = result["chosen_answer"] == answer_dict["answer"].lower()

    proper_articles_are_referred = any(str(article) in answer_dict["context"] for article in result["referred_articles"])
    if answer_is_correct:
        correct_answer_count += 1
        print("Prawidłowa odpowiedź")
    if proper_articles_are_referred is True:
        correct_context_count += 1
        print("Podano prawidłowy kontekst")
    if answer_is_correct and proper_articles_are_referred:
        joint_score += 1
    logger.log_evaluation_result(question_dict, answer_dict, evaluated_answer, answer_is_correct, proper_articles_are_referred, result)

    # evaluated_flow.save_graph_image(path = logger.get_run_directory(evaluated_flow) / "graph.png")


logger.save_end_results(correct_answer_count, correct_context_count, len(questions))

print(f"Liczba prawidłowych odpowiedzi: {correct_answer_count}")
print(f"Liczba prawidłowych odniesień: {correct_context_count}")
print(f"Wynik łączny: {joint_score}")
print(questions_num)
print(context_used)
print(context_used/questions_num)
