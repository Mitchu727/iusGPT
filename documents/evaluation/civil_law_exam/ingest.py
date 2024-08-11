import json
from src.utils.utils import get_project_root

## egzamin adwokacko-radcowski
chosen_dir = get_project_root() / "documents" / "evaluation" / "egzamin_wstepny_adwokacki_radcowski_2023"
questions_path = chosen_dir / "questions.json"
answers_path = chosen_dir / "answers.json"

with open(questions_path, 'r') as f:
    questions = json.load(f)

with open(answers_path, 'r') as f:
    answers = json.load(f)

civil_questions = questions[28:45]
civil_answers = answers[28:45]

## egzamin notarialny
chosen_dir = get_project_root() / "documents" / "evaluation" / "egzamin_wstepny_notarialny_2023"
questions_path = chosen_dir / "questions.json"
answers_path = chosen_dir / "answers.json"

with open(questions_path, 'r') as f:
    questions = json.load(f)

with open(answers_path, 'r') as f:
    answers = json.load(f)

civil_questions.extend(questions[0:29])
civil_answers.extend(answers[0:29])

## egzamin komorniczy
chosen_dir = get_project_root() / "documents" / "evaluation" / "egzamin_wstepny_komorniczy_2023"
questions_path = chosen_dir / "questions.json"
answers_path = chosen_dir / "answers.json"

with open(questions_path, 'r') as f:
    questions = json.load(f)

with open(answers_path, 'r') as f:
    answers = json.load(f)

civil_questions.extend(questions[11:35])
civil_answers.extend(answers[11:35])

## Saving
with open("questions.json", 'w') as f:
    json.dump(civil_questions, f)

with open("answers.json", 'w') as f:
    json.dump(civil_answers, f)