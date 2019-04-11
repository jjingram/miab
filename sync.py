import configparser
import os
import mailbox
import imaplib
import re
import email

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.miabrc'))

maildir = mailbox.Maildir(config['mailbox']['path'])

M = imaplib.IMAP4_SSL(config['server']['hostname'])
M.login(config['login']['user'], config['login']['password'])

list_response_pattern = re.compile(
        r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)'
)

def parse_list_response(line):
    match = list_response_pattern.match(line.decode('utf-8'))
    flags, delimiter, mailbox_name = match.groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

mailboxes = {}
for line in M.list()[1]:
    flags, delimiter, mailbox_name = parse_list_response(line)
    print(flags, delimiter, mailbox_name)
    mailboxes[mailbox_name] = maildir.add_folder(mailbox_name)

for mailbox_name in mailboxes.keys():
    M.select(mailbox_name)
    res, data = M.uid('search', None, 'ALL')
    for uid in data[0].split():
        res, data = M.uid('fetch', uid, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        mailboxes[mailbox_name].add(msg)
    M.close()

M.logout()
