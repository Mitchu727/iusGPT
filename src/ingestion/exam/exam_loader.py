from src.utils.utils import get_project_root

questions_path = get_project_root() / "documents" / "evaluation" / "exam" / "exam.txt"
answers_path = get_project_root() / "documents" / "evaluation" / "exam" / "answers.txt"

with open(questions_path, "r") as f:
    exam_lines = f.readlines()

for i in range(0, len(exam_lines), 5):
    print(exam_lines[i])

with open(answers_path, "r") as f:
    answers_lines = f.readlines()

numerator = 0
for i in range(len(answers_lines)):
    numerator+=1
    question = {
        "question": exam_lines[5*i],
        "possible_answers": exam_lines[5*i + 1: 5*i + 4],
        "answer": answers_lines[i][len(str(numerator)) + 2]
    }
    print(question)
