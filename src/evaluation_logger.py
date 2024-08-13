import csv
import json
import os

from src.flows.flow_interface import FlowInterface
from src.utils.utils import get_runs_directory


class EvaluationLogger:
    def __init__(self, flow: FlowInterface):
        run_directory = self.get_run_directory(flow)

        self.parameters_file_path = run_directory / "parameters.json"
        self.results_json_file_path = run_directory / "results.json"
        self.results_csv_file_path = run_directory / "results.csv"
        self.summary_file_path = run_directory / "summary.json"

        with open(self.parameters_file_path, "w") as f:
            json.dump(flow.get_flow_parameters(), f)

        self.results = []

    def log_evaluation_result(self, question_dict, answer_dict, answer, evaluation_result ):
        result = {
            "dataset": question_dict["dataset"],
            "index": question_dict["index"],
            "question": self.format_question(question_dict),
            "correct_answer_letter": answer_dict["answer"],
            "correct_answer_context": answer_dict["context"],
            "returned_answer": answer,
            "answer_judgment": evaluation_result["answer_is_correct"],
            "context_judgment": evaluation_result["article_is_correct"],
            # "flow"
        }
        self._add_result(result)

    def _add_result(self, result):
        self.results.append(result)
        with open(self.results_json_file_path, "a") as f:
            json.dump(result, f)

        with open(self.results_csv_file_path, "a", newline='') as f:
            csv_writer = csv.writer(f)
            if len(self.results) == 1:
                header = result.keys()
                csv_writer.writerow(header)
            csv_writer.writerow(result.values())


    @staticmethod
    def get_run_directory(flow):
        run_name = flow.get_flow_name()

        run_directory = get_runs_directory() / run_name
        if not os.path.exists(run_directory):
            os.makedirs(run_directory)
            return run_directory
        else:
            numerator = 0
            while os.path.exists(run_directory):
                numerator += 1
                run_directory = get_runs_directory() / f"{run_name}_{numerator}"
            os.makedirs(run_directory)
            return run_directory


    def save_end_results(self, correct_answer_count, correct_context_count, question_number):
        summary = {
            "correct_answer_count": correct_answer_count,
            "correct_context_count": correct_context_count,
            "question_number": question_number
        }
        with open(self.summary_file_path, "w") as f:
            json.dump(summary, f)

    @staticmethod
    def format_question(question_dict):
        return """Question: {question}
    
            a) {answer_a}
            b) {answer_b}
            c) {answer_c}
            """.format(
                question=question_dict["question"],
                answer_a=question_dict["a"],
                answer_b=question_dict["b"],
                answer_c=question_dict["c"]
            )