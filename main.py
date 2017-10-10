import requests
import yaml
import re

config = yaml.load(open("./config.yml"))


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


def split_pdf(path):

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


if __name__ == '__main__':
    main()
