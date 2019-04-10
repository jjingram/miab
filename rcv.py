import configparser
import imaplib

config = configparser.ConfigParser()
config.read('.miabrc')

M = imaplib.IMAP4_SSL(config['server']['hostname'])
M.login(config['login']['user'], config['login']['password'])
M.select()
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print('Message %s\n%s\n' % (num, data[0][1]))
M.close()
M.logout()
