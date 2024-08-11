civil_code_path = "../../documents/civilCodeTxtGenerated/kodeks.txt"
output_path = "../../documents/civilCodeSplitted/kodeks.json"
import json

with open(civil_code_path, "r") as f:
    lines = f.readlines()

book = ""
title = ""
section = ""
chapter = ""
id  = ""
first_index = 0
last_index = 0
articles = []
results = []
for i, line in enumerate(lines):
    chapter_words = ["KSIĘGA", "TYTUŁ", "DZIAŁ", "Rozdział"]
    if any(chapter_word in line for chapter_word in chapter_words):
        if articles:
            result = {
                "id": id,
                "range": [first_index, last_index]
            }
            results.append(result)
            print(id + f" {first_index} {last_index}")
        if "KSIĘGA" in line:
            title = ""
            section = ""
            chapter = ""
            book = line[:-1].replace(" ", "_")
        if "TYTUŁ" in line:
            section = ""
            chapter = ""
            title = line[:-1].replace(" ", "_")
        if "DZIAŁ" in line:
            chapter = ""
            section = line[:-1].replace(" ", "_")
        if "Rozdział" in line:
            chapter = line[:-1].replace(" ", "_")

        id = "".join([book, title, section, chapter])
        # print(id)
        first_index = i + 2
        last_index = i + 1
        articles = []
    else:
        articles.append(line)
        last_index += 1
for result in results:
    result["articles"] = lines[result["range"][0]:result["range"][1]]

with open(output_path, "w+") as f:
    json.dump(results, f)

