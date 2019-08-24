#!/usr/bin/env python3
import smtplib
import psutil
import imaplib
import base64
from email import *
def sendmail(to, text):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    email = 'tomas.storc@afd.cz'
    password = 'Youmb609.'
    send_to_email = to
    subject = 'test' # The subject line
    message = text

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('mail.afd.cz', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()

def getmail():
    email = 'tomas.storc@afd.cz'
    password = 'Youmb609.'
    mail = imaplib.IMAP4_SSL('mail.afd.cz', 993)
    mail.login(email, password)
    mail.select("inbox")
    result, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in range(latest_email_id,first_email_id, -1):
        result, data = mail.fetch(str(i), '(RFC822)' )

        for response_part in data:
            if isinstance(response_part, tuple):
                    # from_bytes, not from_string
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                print ('From : ' + email_from + '\n')
                print ('Subject : ' + email_subject + '\n')
    mail.close()
    mail.logout()            

getmail()
