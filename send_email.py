# coding: utf-8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import pdf_getter
import yaml

def send(toaddr):

    config = yaml.load(open("./config.yml",'r'))

    fromaddr = config['credmails']['addr'] #Configure your emails addr in config.yml

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "[ESGI_Planning]"

    body = "Ne me faites pas me répéter."

    msg.attach(MIMEText(body, 'plain'))

    filename = pdf_getter.main()
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, config['credmails']['password']) #Configure your password addr in config.yml
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def main(file_addr_mail):
    with open(file_addr_mail, 'r') as file_addr_mail:
        for addr_mail in file_addr_mail:
            send(addr_mail.strip())
