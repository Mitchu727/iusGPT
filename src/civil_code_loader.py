import PyPDF2
import re

input_file = "../documents/civilCodePdf/kodeks-cywilny.pdf"
output_file = "../documents/civilCodeTxtGenerated/kodeks.txt"


def remove_kancelaria_sejmu_footnote(text):
    # footNoteRegex = "(?s).{35}[0-9]{4} -[0-9]{2}-[0-9]{2}"
    # footNoteRegex = '\d+'
    footNoteRegex = r"(?s).{35}[0-9]{4} -[0-9]{2}-[0-9]{2} \n "
    cleanedText = re.sub(footNoteRegex, '', text)
    return cleanedText


def split_into_articles(text):
    return text.replace("\n", "").replace("Art.", "\nArt.")


def split_into_chapters(text):
    chapter_words = ["KSIĘGA", "TYTUŁ", "DZIAŁ", "Rozdział"]
    for word in chapter_words:
        text = text.replace(word, "\n"+word)
    return text


def remove_references(text):
    text = text.replace("  1) Niniejsza ustawa dokonuje w  zakresie swojej regulacji transpozycji dyrektywy 2000/31/WE Parlamentu Europejskiego i  Rady z  dnia 8  czerwca 2000  r. w  sprawie niektórych aspektów prawnych usług społeczeństwa informacyjnego, w  szczególności handlu elektronicznego w  ramach rynku wewnętrznego (dyrektywa o  handlu elektronicznym) (Dz. Urz. WE L 178  z 17.07.2000,  str. 1; Dz.  Urz. UE Polskie w ydanie specjalne, rozdz. 13, t.  25, str.  399).  Opracowano na podstawie: t.j. Dz. U. z 2023 r. poz. 1610 , 1615, 1890, 1933 .", "")
    text = text.replace("  2) Z dniem 15  lipca 2006  r. na podstawie wyroku Trybunału Konstytucyjnego z  dnia 15  marca 2005  r. sygn. akt  K 9/04  (Dz. U. poz.  462).", "")
    text = text.replace("  3) Z dniem 18  grudnia 2001  r. na podstawie wy roku T rybunału Konstytucyjnego z  dnia 4  grudnia 2001  r. sygn. akt SK.  18/2000  (Dz. U. poz.  1638).", "")
    text = text.replace("  4) Zdanie drugie utraciło moc z  dniem 23  grudnia 1997  r. na podstawie  obwieszczeni a Prezesa Trybunału Konstyt ucyjnego z  dnia 18  grudnia 1997  r. o utracie mocy  obowiązującej  art. 1 pkt 2, art. 1 pkt 5, art. 2 pkt 2, art. 3 pkt  1 i art. 3 pkt  4 ustawy o  zmianie ustawy o  planowaniu rodziny, ochronie płodu ludzkiego i  warunkach dopuszczalności przerywania ciąży oraz o  zmianie niektórych innych ustaw ( Dz. U. poz.  1040). § 2. W przypadkach określonych w  art. 445 § 1 i 2 oraz art.  4462 ten, czyje d obro osobiste zostało naruszone, może obok zadośćuczynienia pieniężnego żądać zasądzenia odpowiedniej sumy na wskazany przez niego cel społeczny.  § 3. Do roszczeń, o  których mowa w  § 1 i 2, przepis art.  445 § 3 stosuje się.  ", "")
    text = text.replace("  5) Utracił moc z  dniem 14  lutego 2001  r. w zakresie, w  którym odnosi się do spadków otwartych od dnia 14 lutego 2001  r., na podstawie  wyroku Trybunału Konstytucyjnego z  dnia 31  stycznia 2001  r. sygn. akt P. 4/99  (Dz. U. poz.  91).", "")
    text = text.replace("  6) Utracił moc z  dniem 14  lutego 2001  r. w zakresie, w  którym odnosi się do spadków otwartych od dnia 14 lutego 2001  r., na podstawie  wyroku Trybunału Konstytucyjnego, o  którym mo wa w  odnośniku 5. ©gospodarstwa dziedziczyć dla braku warunków przewidzianych w  art. 1059. Przepis ten stosuje się odpowiednio do dalszych zstępnych.", "")
    text = text.replace("  7) Utracił moc z  dniem 14  lutego 2001  r. w zakresie, w  którym odnosi się do spadków otwartych od dnia 14 lutego 2001  r., na podstawie  wyroku Trybunału Konstytucyjnego,  o którym mowa w  odnośniku 5. 8) Utracił moc z  dniem 14  lutego 2001  r. w zakresie, w  którym odnosi się do spadków otwartych od dnia 14 lutego 2001  r., na podstawie  wyroku Trybunału Konstytucyjnego, o  którym  mowa w  odnośniku 5. ©", "")
    text = text.replace("  8) Utracił moc z  dniem 14  lutego 2001  r. w zakresie, w  którym odnosi się do spadków otwartych od dnia 14 lutego 2001  r., na podstawie  wyroku Trybunału Konstytucyjnego, o  którym  mowa w  odnośniku 5. ©", "")
    text = text.replace("  9) Utracił moc z  dniem 14  lutego 2001  r. w zakresie, w  którym odnosi się do spadków otwartych od dnia 14 lutego 2001  r., na po dstawie  wyroku Trybunału Konstytucyjnego,  o którym m owa w odnośniku  5. ", "")
    text = text.replace("\nArt. 179. (utracił moc)2) ", "")
    text = text.replace("\nArt. 418. (utracił moc)3) ", "")
    text = text.replace("Art. 4461.4)", "Art. 4461. ")
    text = text.replace("Art. 1059.5)", "Art. 1059. ")
    text = text.replace("Art. 1060.6)", "Art. 1060. ")
    text = text.replace("Art. 1062.7)", "Art. 1062. ")
    text = text.replace("Art. 1064.8)", "Art. 1064. ")
    text = text.replace("Art. 1087.9)", "Art. 1087. ")
    return text


def filter_abolished(text):
    articles = text.split("\n")
    filtered_articles = [article for article in articles if "uchylony" not in article]
    return "\n".join(filtered_articles)


def remove_first_line(text):
    return "\n".join(text.split("\n")[1:])

# creating a pdf file object
if __name__ == "__main__":
    pdfFileObj = open(input_file, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    with open(output_file, "w+") as f:
        # for page in pdfReader.pages[9:13]:
        #     text = page.extract_text()
        #     cleanedText = removeKancelariaSejmuFootNote(text)
        #     f.write(cleanedText)
        # text = ''.join([page.extract_text() for page in pdfReader.pages[0:40]])
        text = ''.join([page.extract_text() for page in pdfReader.pages])
        text = split_into_articles(remove_kancelaria_sejmu_footnote(text))
        text = split_into_chapters(text)
        text = remove_references(text)
        text = filter_abolished(text)
        text = remove_first_line(text)
        f.write(text)


        # closing the pdf file object
    pdfFileObj.close()