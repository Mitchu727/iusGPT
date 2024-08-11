import regex as re
import json
input_file = "source.txt"
lookup_file = "lookup.txt"
output_file = "source.json"

with open(input_file, "r") as f:
    text = f.read()


def extract_id_from_article(article_text):
    return re.search(r"Art\. [0-9]+\.", article_text).group()


text = text.replace("""©Kancelaria Sejmu s. 1/236
2024-07-23
Dz. U. 1964 Nr 16 poz. 93
U S T A W A
z dnia 23 kwietnia 1964 r.
Kodeks cywilny1)
""", "")
text = text.replace("""1) Niniejsza ustawa dokonuje w zakresie swojej regulacji transpozycji dyrektywy 2000/31/WE
Parlamentu Europejskiego i Rady z dnia 8 czerwca 2000 r. w sprawie niektórych aspektów
prawnych usług społeczeństwa informacyjnego, w szczególności handlu elektronicznego w ramach
rynku wewnętrznego (dyrektywa o handlu elektronicznym) (Dz. Urz. WE L 178 z 17.07.2000,
str. 1; Dz. Urz. UE Polskie wydanie specjalne, rozdz. 13, t. 25, str. 399).
Opracowano na
podstawie: t.j.
Dz. U. z 2024 r.
poz. 1061.
""", "")
text = text.replace("""2) Z dniem 15 lipca 2006 r. na podstawie wyroku Trybunału Konstytucyjnego z dnia 15 marca 2005 r.
sygn. akt K 9/04 (Dz. U. poz. 462).
""", "")
text = text.replace("""3) Z dniem 18 grudnia 2001 r. na podstawie wyroku Trybunału Konstytucyjnego z dnia 4 grudnia
2001 r. sygn. akt SK. 18/2000 (Dz. U. poz. 1638).
""", "")
text = text.replace("""4) Zdanie drugie utraciło moc z dniem 23 grudnia 1997 r. na podstawie obwieszczenia Prezesa
Trybunału Konstytucyjnego z dnia 18 grudnia 1997 r. o utracie mocy obowiązującej art. 1 pkt 2,
art. 1 pkt 5, art. 2 pkt 2, art. 3 pkt 1 i art. 3 pkt 4 ustawy o zmianie ustawy o planowaniu rodziny,
ochronie płodu ludzkiego i warunkach dopuszczalności przerywania ciąży oraz o zmianie
niektórych innych ustaw (Dz. U. poz. 1040).
""", "")


text = re.sub(r"[0-9]\) Utracił moc (.|\n)*? odnośniku( |\n)5.", '', text)
text = re.sub(r".Kancelaria Sejmu s. .*\n[0-9]{4}-[0-9]{2}-[0-9]{2}\n", '', text)

text = re.sub(r'(KSIĘGA [^\n]+)\n', r'\n\1 ', text)
text = re.sub(r'(TYTUŁ [^\n]+)\n', r'\n\1 ', text)
text = re.sub(r'(DZIAŁ [^\n]+)\n', r'\n\1 ', text)
text = re.sub(r'(Rozdział [^\n]+)\n', r'\n\1 ', text)
text = re.sub(r'Oddział .*\n.*\n', ' ', text)
text = re.sub(r'\nArt. [0-9]*\. \(uchylony\)', '', text)

text = text.replace("Art.", "\nArt.")

with open(lookup_file, "w+") as f:
    f.write(text)

book = ""
title = ""
section = ""
chapter = ""
articles = []
for element in text.split("\n\n"):
    if "KSIĘGA" in element:
        book = element
        title = ""
        section = ""
        chapter = ""
    if "TYTUŁ" in element:
        title = element
        section = ""
        chapter = ""
    if "DZIAŁ" in element:
        section = element
        chapter = ""
    if "Rozdział" in element:
        chapter = element
    if element.startswith("Art."):
        article = {
            "id": extract_id_from_article(element),
            "book": book,
            "title": title,
            "section": section,
            "chapter": chapter,
            "content": element
        }
        articles.append(article)

with open(output_file, "w+") as f:
    json.dump(articles, f)
