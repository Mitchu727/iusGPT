import json

from src.evaluation_logger import EvaluationLogger
from src.flows.concept_flow.concept_flow import ConceptFlow
from src.flows.multi_agent_flow import MultiAgentFlow
from src.flows.simple_flow import SimpleFlow
from src.flows.simple_rag_flow import SimpleRagFlow
from src.flows.simple_rag_search_flow import SimpleRagSearchFlow
from src.utils.utils import get_project_root, format_question, format_answer
from src.flows.judge import Judge
from langchain_community.callbacks import get_openai_callback
import random


def load_questions_for_codes(code_list):
    questions = []
    answers = []
    for code in code_list:
        dataset_path = get_project_root() / "documents" / "evaluation" / code
        questions_path = dataset_path / "questions.json"
        answers_path = dataset_path / "answers.json"
        with open(questions_path, "r") as f:
            code_questions = json.load(f)
        questions.extend(code_questions)
        with open(answers_path, "r") as f:
            code_answers = json.load(f)
        answers.extend(code_answers)
    return questions, answers


# dataset_path = get_project_root() / "documents" / "evaluation" / "penal_code_questions"
questions, answers = load_questions_for_codes(["civil_code"])

# evaluated_flow = SimpleFlow("gpt-4", 0)  # 83, 97
# evaluated_flow = SimpleFlow("gpt-4o", 0)  # 83, 97
# evaluated_flow = SimpleFlow("gpt-4o-mini", 0)  # 83, 97
# evaluated_flow = SimpleFlow("gpt-3.5-turbo-0125", 0)  # 25, 7

evaluated_flow = SimpleRagSearchFlow("gpt-3.5-turbo-0125", 0, 50)
# evaluated_flow = SimpleRagSearchFlow("gpt-4o-mini", 0, 50)

# evaluated_flow = SimpleFlow("gpt-4o-mini", 0)  # 46, 38
# evaluated_flow = SimpleRagFlow("gpt-4o-mini", 0, 50)

# evaluated_flow = SimpleFlow("gpt-3.5-turbo-0125", 0)  # 46, 38
# evaluated_flow = SimpleRagFlow("gpt-3.5-turbo-0125", 0, 50)

# evaluated_flow = MultiAgentFlow("gpt-4o-mini", 0, 50)

# evaluated_flow = SimpleFlow("gpt-4", 0)  # 46, 38

# evaluated_flow = SimpleRagSearchFlow("gpt-3.5-turbo-0125", 0, 30) # 11, 4
# evaluated_flow = MultiAgentFlow("gpt-3.5-turbo-0125", 0, 30)
# evaluated_flow = SimpleRagFlow("gpt-3.5-turbo-0125", 0, 30)  # 30, 38

# evaluated_flow = SimpleRagFlow("gpt-4o", 0)  # 59, 63
# evaluated_flow = SimpleRagFlow("gpt-4o-mini", 0, 30)  # 56, 52  # 116, 114

judge = Judge("gpt-4o-mini", 0)

logger = EvaluationLogger(evaluated_flow)
context_used = 0
correct_answer_count = 0
correct_context_count = 0
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
            evaluated_answer = evaluated_flow.answer_evaluation_question(question_dict)
            print("==========KOSZTY==========")
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            context_used += cb.total_tokens
        evaluation_result = judge.assess_evaluation_question(question_dict, answer_dict, evaluated_answer)
        result = json.loads(evaluation_result)
    except:
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
    logger.log_evaluation_result(question_dict, answer_dict, evaluated_answer, answer_is_correct, proper_articles_are_referred, result)

    # evaluated_flow.save_graph_image(path = logger.get_run_directory(evaluated_flow) / "graph.png")


logger.save_end_results(correct_answer_count, correct_context_count, len(questions))

print(correct_answer_count)
print(correct_context_count)
print(questions_num)
print(context_used)
print(context_used/questions_num)
