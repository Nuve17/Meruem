from pyPdf import PdfFileWriter, PdfFileReader
from os import rename, listdir, path, makedirs
from datetime import datetime, date
import arrow
import glob
import sys
import requests
import yaml
import re

config = yaml.load(open("../config.yml"))


def change_name(PdfDescriptor):
    reader = PdfFileReader(PdfDescriptor)
    contents = reader.getPage(0).extractText()
    year=contents.split('ESGI')[1][-7:][1:5]
    date=contents.split('lundi ')[1][:5]+"/"+year
    return date.replace('/','-')

def get_cookies():
    rx_lt = 'value="[a-zA-Z0-9\-]*"'
    rx_lt = re.compile(rx_lt)
    request = requests.get("https://cas-sso.reseau-ges.fr/login")
    cookies = request.cookies
    lt = rx_lt.findall(request.content)[2]
    return cookies, lt[7:-1]


def get_pdf(url, cookies):
    try:
        file_name = "./PlanningAnnuel5ASI2.pdf"
        pdf_file = requests.get(url, cookies=cookies, allow_redirects=True, stream=True)
        data = pdf_file.content
        with open(file_name, 'wb') as PlanningFile:
            PlanningFile.write(data)
        return file_name
    except Exception as e:
        return str(e)


def split_pdf(path_pdf):

    inputpdf = PdfFileReader(file(path_pdf, "rb"))
    inputpdf.decrypt('')

    if not path.exists('./tmp'):
        makedirs('./tmp/')

    for i in range(inputpdf.numPages // 1):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i * 1))
        if i * 2 + 1 <  inputpdf.numPages:
            output.addPage(inputpdf.getPage(i))
        newname =path_pdf[:7] + "-" + str(i) + ".pdf"
        outputStream = file( "./tmp/"+newname, "w+")
        output.write(outputStream)
        DateName=change_name(outputStream)
        outputStream.close()
        rename("./tmp/"+newname, "./tmp/"+DateName)

    AllPdf=listdir('./tmp/')
    now=datetime.now()
    now=now.strftime('%Y-%m-%d')
    DateNow=arrow.get(now)

    for pdf in AllPdf:
        PdfReturn=pdf.split('-')
        PdfReturn=PdfReturn[::-1]
        PdfDate='-'.join(PdfReturn)

        DateFile=arrow.get(pdf)
        print DateNow
        print DateFile
        delta= (DateFile-DateNow)
        print now
        print PdfDate
        print delta.days

    return True


def main():
    rx_success = re.compile("\<div id\=\"msg\" class\=\"success\"\>")
    rx_planning = re.compile("href.*Semestre")
    cookies, lt = get_cookies()
    data = config['credentials']
    data.update({"lt": lt})
    data.update({"execution": "e1s1"})
    data.update({"_eventId": "submit"})
    data.update({"submit": "CONNEXION"})

    print(cookies)
    request = requests.post("https://cas-sso.reseau-ges.fr/login", data=data, cookies=cookies, allow_redirects=True)

    if rx_success.search(request.content):
        cookies = request.cookies
        student_page = requests.get('http://www.myges.fr/common/student-documents', cookies=cookies, allow_redirects=True)
        html = student_page.text
        planning = rx_planning.search(html)
        if rx_planning.search(student_page.text):
            pdf_link = rx_planning.findall(html)[0][6:-19]
            filename = get_pdf(pdf_link, cookies)
            pdf_recent=split_pdf(filename)

if __name__ == '__main__':
    main()
