import configparser
import imaplib
import email

config = configparser.ConfigParser()
config.read('.miabrc')

M = imaplib.IMAP4_SSL(config['server']['hostname'])
M.login(config['login']['user'], config['login']['password'])

inbox = []
M.select('INBOX', True)
typ, data = M.uid('sort', '(FROM DATE)', 'UTF-8', 'ALL')
for uid in data[0].split():
    typ, data = M.uid('fetch', uid, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    inbox.append(msg)
for msg in inbox:
    print(msg)
M.close()

sent = []
M.select('Sent', True)
typ, data = M.uid('sort', '(TO DATE)', 'UTF-8', 'ALL')
for uid in data[0].split():
    typ, data = M.uid('fetch', uid, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    sent.append(msg)
for msg in sent:
    print(msg)
M.close()

M.logout()
