import codecs


def _remove_breaklines(string):
    return ' '.join(string.splitlines())


class CasesLoader:
    default_path = "../cases"

    def __init__(self, path=default_path):
        self.path = path

    def load_case(self, case_number):
        path = self._get_case_path(case_number)
        with codecs.open(path, "r", 'utf-8') as f:
            content = f.read()
        content = _remove_breaklines(content)
        return content

    def load_questions(self, case_number):
        path = self._get_questions_path(case_number)
        with codecs.open(path, "r", 'utf-8') as f:
            questions = f.read()
        return questions.split("\r\n")

    def load_regulations(self, case_number):
        path = self._get_regulations_path(case_number)
        with codecs.open(path, "r", 'utf-8') as f:
            regulations = f.read()
        return regulations.split("\r\n")

    def _get_case_path(self, case_number):
        return f"{self.path}/{case_number}/case.txt"

    def _get_questions_path(self, case_number):
        return f"{self.path}/{case_number}/questions.txt"

    def _get_regulations_path(self, case_number):
        return f"{self.path}/{case_number}/regulations.txt"


# # EXPERIMENT
if __name__ == "__main__":
    loader = CasesLoader()
    some_string = "Jan K. zawarł umowę o pracę z radcą prawnym Grzegorzem J. Strony zawarły umowę na czas nieokreślony, ustanawiając wynagrodzenie aplikanta na najniższe wynagrodzenie krajowe. Grzegorz J. zawarł następnie z aplikantem umowę, na mocy której wyraził zgoe na odbywanie przez Jana K.,w czasie trwania zatrudnienia, aplikacji radcowskiej i zobowiązał się w związku z tym do udzielenia Janowi K. płatnego urlopu szkoleniowego,a ponadto uiszczenia części kosztów aplikacji. W zamian za to aplikant zobowiązał się przepracowaću Grzegorza J. trzy lata od chwili ukończeniaaplikacji. Strony przewidziały w umowie, że w razie wcześniejszego wypowiedzenia umowy o pracę przez pracodawcę, a także w razie rozwiązaniaumowy o pracę przez pracodawcę z winy pracownika lub wygaśnięcia umowy o pracę wskutek porzucenia pracy przez pracownika, pracownik będziezobowiązany do zwrotu pracodawcy poniesionych przez niego kosztów aplikacji radcowskiej oraz do zapłaty odszkodowania.Jan K. ukończył aplikacje radcowską i zdał egzamin radcowski. Zwrócił się do Grzegorza J. o wyrażenie zgody na rozwiązanie umowy o pracę. Grzegorz J. domaga się zapłaty odszkodowana, lecz Jan K. zwrócił mu jedynie poniesione koszty aplikacji, natomiast odmówił zapłaty odszkodowania."
    print(loader.load_case(1))
    print(some_string)
    # print(some_string)
    # print(loader.load_regulations(1))
