from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("document.pdf", "rb"))
subjects = {}
previousIndex = -1
j = -1
for i in range(inputpdf.numPages):
    if i == 0:
        continue
    try:
        s = inputpdf.getPage(i).extractText().lstrip().rstrip()
        startIndex = s.find("Subject: ")
        if startIndex != -1:
            endIndex = s.find("Teacher:",startIndex)
            if endIndex != -1:
                subject = s[startIndex + 9:endIndex].lstrip().rstrip().replace("\n","")
                if not subject in subjects:
                    subjects[subject] = PdfFileWriter()
                output = subjects[subject]
                output.addPage(inputpdf.getPage(i))
        if startIndex == -1 and previousIndex != -1 and j == (i - 1) and s != "":
            check = s.find("Subject Report")
            if subject in subjects and check == -1:
                output = subjects[subject]
                output.addPage(inputpdf.getPage(i))
    except:
        previousIndex = -1
        #print("Skipped Page " + str(i))
    finally:
        j = i
        previousIndex = startIndex

for subject in subjects:
    output = subjects[subject]
    with open(subject + ".pdf", "wb") as outputStream:
        output.write(outputStream)
