#!/usr/bin/python3
import smtplib
import psutil
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

def notify(app):
    for proc in psutil.process_iter():
        if proc.name() in app:
            sendmail('tomas.storc@gmail.com', 'there is app {} running on your pc'.format(app))

notify('firefox')
