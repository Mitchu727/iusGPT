import os

import regex as re
import json

from src.utils.utils import get_project_root

list_of_directories = [directory for directory in os.listdir() if directory[-3:] != ".py"]
# list_of_directories = ["penal_code", "labor_code"]
for dir_name in list_of_directories[:1]:
    print(dir_name)
    dir_path = get_project_root() / "documents" / "legal_acts" / "batch" / dir_name
    json_file_path = dir_path / "source.json"
    txt_file_path = dir_path / "source.txt"
    lookup_file_path = dir_path / "lookup.txt"
    with open(txt_file_path, "r", encoding="UTF-8") as f:
        text = f.read()

    text = re.sub(r"((\n|.)*?)(CZĘŚĆ|DZIAŁ|TYTUŁ)", r"\3", text, 1)
    text = re.sub(r"( |\n)*©Kancelaria Sejmu(.|\n)*?[0-9]{4}-[0-9]{2}-[0-9]{2}( |)*", "", text)
    text = re.sub(r"\n *\n(\S.*\n)*.*(Niniejsza ustawa|Utracił moc|wyroku \n*Trybunału \n*Konstytucyjnego|Zmiany tekstu jednolitego|Zmiany wymienionego rozporządzenia|Zmiana wymienionego rozporządzenia| Zmiany wymienionej ustawy).*\n(.*\n)*?(\S.*\n)*", "", text)

    with open(lookup_file_path, "w+", encoding="UTF-8") as f:
        f.write(text)
    # \n *\n[0 - 9] +\)(.| \n(?!§)) * ?\n *\n

    # \n *\n[0-9]+\)(.\n*)*?(Utracił moc|wyroku Trybunału Konstytucyjnego|Zmiany tekstu jednolitego|Zmiany wymienionego rozporządzenia)(.|\n)*?\n *\n