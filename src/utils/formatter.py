import json
from openpyxl import Workbook
import pandas as pd

def from_json_to_xlsx(json_file, xlsx_file):
    experiments = pd.read_json(json_file)
    experiments.to_excel(xlsx_file)
