import json

from src.evaluation_logger import EvaluationLogger
from src.flows.chunk_flow.article_generator import ArticleKnowledgeGenerator
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


# TODO
#  - Knowledge graph -> to ładnie wyląda
#  - kartkowanie -> to jest oryginalne i tego chciałby promotor
#  - strojenie promptów do react'a + dodanie narzędzi -> rozwinięcie react'a które dałoby się obronić

article_knowledge_generator = ArticleKnowledgeGenerator()

correct_answer_count = 0
correct_article_count = 0
for i in range(25):
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
        # evaluated_answer = .answer_evaluation_question(question_dict)
        response = article_knowledge_generator.generate_article_knowledge(question_dict)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    print("==========ODPOWIEDŹ==========")
    print(response)
    # print(evaluated_answer)



# TODO
# refactor
# k-means na embeddingach