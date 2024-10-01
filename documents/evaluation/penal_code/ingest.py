import json
from src.utils.utils import get_project_root

code_questions = []
code_answers = []

def get_questions_and_answers_from_directory(directory, lower_index, upper_index):
    chosen_dir = get_project_root() / "documents" / "evaluation" / directory
    questions_path = chosen_dir / "questions.json"
    answers_path = chosen_dir / "answers.json"

    with open(questions_path, 'r') as f:
        questions_from_file = json.load(f)

    with open(answers_path, 'r') as f:
        answers_from_file = json.load(f)

    for question in questions_from_file:
        question["dataset"] = directory

    for answer in answers_from_file:
        answer["dataset"] = directory

    return questions_from_file[lower_index:upper_index], answers_from_file[lower_index:upper_index]


## ROK 2022
## egzamin adwokacko-radcowski
questions, answers = get_questions_and_answers_from_directory("egzamin_wstepny_adwokacki_radcowski_2022", 0, 11)
code_questions.extend(questions)
code_answers.extend(answers)

# ## egzamin notarialny nie ma pytań z karnego
# questions, answers = get_questions_and_answers_from_directory("egzamin_wstepny_notarialny_2022", 0, 30)
# civil_questions.extend(questions)
# civil_answers.extend(answers)

## egzamin komorniczy
questions, answers = get_questions_and_answers_from_directory("egzamin_wstepny_komorniczy_2022", 72, 76)
code_questions.extend(questions)
code_answers.extend(answers)

## ROK 2023
## egzamin adwokacko-radcowski
questions, answers = get_questions_and_answers_from_directory("egzamin_wstepny_adwokacki_radcowski_2023", 0, 11)
code_questions.extend(questions)
code_answers.extend(answers)

# ## egzamin notarialny nie ma pytań z karnego
# questions, answers = get_questions_and_answers_from_directory("egzamin_wstepny_notarialny_2023", 0, 29)
# civil_questions.extend(questions)
# civil_answers.extend(answers)

## egzamin komorniczy
questions, answers = get_questions_and_answers_from_directory("egzamin_wstepny_komorniczy_2023", 72, 76)
code_questions.extend(questions)
code_answers.extend(answers)

print(len(code_questions))

## Saving
with open("questions.json", 'w') as f:
    json.dump(code_questions, f)

with open("answers.json", 'w') as f:
    json.dump(code_answers, f)