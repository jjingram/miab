import configparser
import smtplib
import imaplib
from email.message import EmailMessage
import time

config = configparser.ConfigParser()
config.read('.miabrc')

def prompt(prompt):
    return input(prompt).strip()

fromaddr = config['login']['user']
toaddrs  = prompt("To: ").split()
print("Enter message, end with ^D (Unix) or ^Z (Windows):")

msg = EmailMessage()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddrs)

body = ''
while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    body = body + line
msg.set_content(body)

S = smtplib.SMTP(config['server']['hostname'], config['server']['port'])
S.set_debuglevel(1)
S.starttls()
S.login(config['login']['user'], config['login']['password'])
S.send_message(msg)
S.quit()

M = imaplib.IMAP4_SSL(config['server']['hostname'])
M.debug = 4
M.login(config['login']['user'], config['login']['password'])
M.append('Sent', '', imaplib.Time2Internaldate(time.time()), str(msg).encode('utf-8'))
M.logout()
