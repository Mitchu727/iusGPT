import json
from openpyxl import Workbook


def from_json_to_xlsx(json_file, xlsx_file):

    with open(json_file) as f:
        experiments = json.load(f)

    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "Question"
    sheet["B1"] = "Answer"

    index = 2
    for experiment in experiments:
        sheet["A"+str(index)] = experiment['query']
        sheet["B"+str(index)] = experiment['answer']
        index += 1

    workbook.save(xlsx_file)

    #     markdown_string += f"|{experiment['query']}|{experiment['answer']}|\n"
    # print(markdown_string)



#     markdown_string = """
# | Question    | Answer |
# | -------- | ------- |
# """