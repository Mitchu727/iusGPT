import PyPDF2
import re

inputFile = "../documents/civilCodePdf/kodeks-cywilny.pdf"
outputFile = "../documents/civilCodeTxtGenerated/kodeks.txt"

def removeKancelariaSejmuFootNote(text):
    # footNoteRegex = "(?s).{35}[0-9]{4} -[0-9]{2}-[0-9]{2}"
    # footNoteRegex = '\d+'
    footNoteRegex = r"(?s).{35}[0-9]{4} -[0-9]{2}-[0-9]{2} \n "
    cleanedText = re.sub(footNoteRegex, '', text)
    return cleanedText

def fitArticlesIntoLines(text):
    return text.replace("\n", "").replace("Art.", "\nArt.")

# creating a pdf file object
if __name__ == "__main__":
    pdfFileObj = open(inputFile, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    with open(outputFile, "w+") as f:
        # for page in pdfReader.pages[9:13]:
        #     text = page.extract_text()
        #     cleanedText = removeKancelariaSejmuFootNote(text)
        #     f.write(cleanedText)
        text = ''.join([page.extract_text() for page in pdfReader.pages[9:13]])
        cleanedText = fitArticlesIntoLines(removeKancelariaSejmuFootNote(text))
        f.write(cleanedText)


        # closing the pdf file object
    pdfFileObj.close()