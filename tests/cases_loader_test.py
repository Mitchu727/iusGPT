import unittest
from src.cases_loader import CasesLoader

class CasesLoaderTest(unittest.TestCase):
    loader = CasesLoader()
    
    def test_case_loading(self):
        assert self.loader.load_case(1) == "Jan K. zawarł umowę o pracę z radcą prawnym Grzegorzem J. Strony zawarły umowę na czas nieokreślony, ustanawiając wynagrodzenie aplikanta na najniższe wynagrodzenie krajowe. Grzegorz J. zawarł następnie z aplikantem umowę, na mocy której wyraził zgodę na odbywanie przez Jana K., w czasie trwania zatrudnienia, aplikacji radcowskiej i zobowiązał się w związku z tym do udzielenia Janowi K. płatnego urlopu szkoleniowego, a ponadto uiszczenia części kosztów aplikacji. W zamian za to aplikant zobowiązał się przepracowaću Grzegorza J. trzy lata od chwili ukończenia aplikacji. Strony przewidziały w umowie, że w razie wcześniejszego wypowiedzenia umowy o pracę przez pracodawcę, a także w razie rozwiązania umowy o pracę przez pracodawcę z winy pracownika lub wygaśnięcia umowy o pracę wskutek porzucenia pracy przez pracownika, pracownik będzie zobowiązany do zwrotu pracodawcy poniesionych przez niego kosztów aplikacji radcowskiej oraz do zapłaty odszkodowania. Jan K. ukończył aplikacje radcowską i zdał egzamin radcowski. Zwrócił się do Grzegorza J. o wyrażenie zgody na rozwiązanie umowy o pracę. Grzegorz J. domaga się zapłaty odszkodowana, lecz Jan K. zwrócił mu jedynie poniesione koszty aplikacji, natomiast odmówił zapłaty odszkodowania."

    def test_questions_loading(self):
        assert self.loader.load_questions(1) == [
            "Czy zawarta umowa jest ważna?",
            "Jak należy zakwalifikować takie postanowienie umowne?",
            "Czy Jan K. może się zwolnić z obowiązku zapłaty odszkodowania?"
        ]

    def test_regulations_loading(self):
        assert self.loader.load_regulations(1) == ["art. 353^1 k.c.", "art. 365 k.c."]


if __name__ == '__main__':
    unittest.main()
