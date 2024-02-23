import json
from openpyxl import Workbook

if __name__ == "__main__":
    with open("experiments.json") as f:
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


    workbook.save("experiments.xlsx")

    #     markdown_string += f"|{experiment['query']}|{experiment['answer']}|\n"
    # print(markdown_string)



#     markdown_string = """
# | Question    | Answer |
# | -------- | ------- |
# """