import configparser
import imaplib
import email

config = configparser.ConfigParser()
config.read('.miabrc')

M = imaplib.IMAP4_SSL(config['server']['hostname'])
M.login(config['login']['user'], config['login']['password'])

recv = []
M.select('INBOX', True)
typ, data = M.uid('search', None, '(Header "Email2Chat-Version" "")')
for uid in data[0].split():
    typ, data = M.uid('fetch', uid, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    recv.append(msg)
for msg in recv:
    print(msg)

sent = []
M.select('Sent', True)
typ, data = M.uid('search', None, '(Header "Email2Chat-Version" "")')
for uid in data[0].split():
    typ, data = M.uid('fetch', uid, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    sent.append(msg)
for msg in sent:
    print(msg)

M.close()
M.logout()
