import json
import re

# ## Answers extraction
answers_input_file = "answers.txt"
answers_output_file = "answers.json"

with open(answers_input_file, "r", encoding="utf-8") as f:
    answers_raw = f.read()

answers_raw = answers_raw.replace("""WYKAZ PRAWIDŁOWYCH ODPOWIEDZI DO ZESTAWU PYTAŃ TESTOWYCH 
NA EGZAMIN WSTĘPNY NA APLIKACJĘ NOTARIALNĄ
24 WRZEŚNIA 2022 R.

nr pytania	prawidłowa odpowiedź	podstawa prawna
""", "")

answers_raw = re.sub("\n[0-9]\n", "\n", answers_raw)
answers_raw = re.sub("\n(?![0-9]+)", " ", answers_raw)
answers_raw = re.sub("Aart\.", "A art.", answers_raw)
answers_raw = re.sub("Bart\.", "B art.", answers_raw)
answers_raw = re.sub("Cart\.", "C art.", answers_raw)

answers_rows = answers_raw.split("\n")

answers = []
for i, answers_row in enumerate(answers_rows):
    question_index_offset = len(str(i+1))

    answer = {
        "index": i+1,
        "answer": answers_row[question_index_offset+2],
        "context": answers_row[question_index_offset+4:],
    }
    answers.append(answer)


with open(answers_output_file, "w") as f:
    json.dump(answers, f)


## Questions extraction
questions_input_file = "questions.txt"
questions_output_file = "questions.json"
with open(questions_input_file, "r", encoding="utf-8") as f:
    questions_raw = f.read()


questions_raw = questions_raw.replace(""" Ministerstwo Sprawiedliwości
Departament Zawodów Prawniczych

EGZAMIN WSTĘPNY
DLA KANDYDATÓW NA APLIKANTÓW
NOTARIALNYCH
24 WRZEŚNIA 2022 r.

ZESTAW PYTAŃ TESTOWYCH


Pouczenie:

 1.	Zestaw pytań testowych i kartę odpowiedzi oznacza się indywidualnym kodem. Wylosowany numer kodu kandydat wpisuje w prawym górnym rogu na pierwszej stronie zestawu pytań testowych i na każdej stronie karty odpowiedzi. Nie jest dopuszczalne w żadnym miejscu zestawu pytań testowych i karty odpowiedzi wpisanie imienia i nazwiska ani też podpisanie się własnym imieniem i nazwiskiem. 
	
	Karta odpowiedzi bez prawidłowo zamieszczonego oznaczenia kodowego nie podlega ocenie Komisji Kwalifikacyjnej. 

 2.	Każdy kandydat otrzymuje:
	1) jeden egzemplarz zestawu pytań testowych, zawarty na 36 stronach; 
	2) jeden egzemplarz karty odpowiedzi, zawarty na 4 stronach.

 3.	Przed przystąpieniem do rozwiązania zestawu pytań testowych należy sprawdzić, czy zawiera on wszystkie kolejno ponumerowane strony od 1 do 36 oraz czy karta odpowiedzi zawiera 4 strony. W przypadku braku którejkolwiek ze stron, należy 
o tym niezwłocznie zawiadomić Komisję Kwalifikacyjną.

 4.	Zestaw pytań testowych składa się ze 150 pytań jednokrotnego wyboru, przy czym każde pytanie zawiera po 3 propozycje odpowiedzi. 
	Wybór odpowiedzi polega na zakreśleniu na karcie odpowiedzi znakiem „X” jednej z trzech propozycji odpowiedzi w odpowiedniej kolumnie (A albo B, albo C). 
	Prawidłowa jest odpowiedź, która w połączeniu z treścią pytania tworzy – w świetle obowiązującego prawa – zdanie prawdziwe. Na każde pytanie testowe tylko jedna odpowiedź jest prawidłowa. Niedopuszczalne jest dokonywanie dodatkowych założeń, wykraczających poza treść pytania.

 5.	Wyłączną podstawę ustalenia wyniku kandydata stanowią odpowiedzi zakreślone na karcie odpowiedzi. Odpowiedzi zaznaczone na zestawie pytań testowych nie będą podlegały ocenie. 

 6.	Zmiana zakreślonej odpowiedzi jest niedozwolona. 

 7.	Za każdą prawidłową odpowiedź kandydat otrzymuje 1 punkt. W przypadku zaznaczenia więcej niż jednej odpowiedzi, żadna z odpowiedzi nie podlega zaliczeniu jako prawidłowa. 

 8.	Prawidłowość odpowiedzi ocenia się według stanu prawnego na dzień 24 września 2022 r.

9.	Czas na rozwiązanie zestawu pytań testowych wynosi 150 minut (wyjątek: wydłużenie czasu egzaminu dla kandydata będącego osobą niepełnosprawną).
""", "")

questions_raw = re.sub("[0-9]+ EGZAMIN WSTĘPNY DLA KANDYDATÓW NA APLIKANTÓW NOTARIALNYCH\n", "", questions_raw)
questions_raw = re.sub("EGZAMIN WSTĘPNY DLA KANDYDATÓW NA APLIKANTÓW NOTARIALNYCH [0-9]+\n", "", questions_raw)
questions_raw = re.sub("\n(?!(A\.|B\.|C\.|[0-9]+\.))", " ", questions_raw)

questions_lines = questions_raw.split("\n")
print(questions_raw)

questions = []
for i in range(150):
    question_index_offset = len(str(i + 1))

    question = {
        "index": i+1,
        "question": questions_lines[4*i][question_index_offset+2:],
        "a": questions_lines[4*i+1][3:-1],
        "b": questions_lines[4*i+2][3:-1],
        "c": questions_lines[4*i+3][3:-1]
    }

    questions.append(question)

with open(questions_output_file, "w") as f:
    json.dump(questions, f)
