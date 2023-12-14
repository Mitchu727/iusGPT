import PyPDF2

inputFile = "../documents/civilCodePdf/kodeks-cywilny.pdf"
outputFile = "../documents/civilCodeTxtGenerated/kodeks.txt"

# creating a pdf file object
if __name__ == "__main__":
    pdfFileObj = open(inputFile, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    with open(outputFile, "w+") as f:
        for page in pdfReader.pages:
            f.write(page.extract_text())

    # closing the pdf file object
    pdfFileObj.close()