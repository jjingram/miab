import configparser
import smtplib

config = configparser.ConfigParser()
config.read('.miabrc')

def prompt(prompt):
    return input(prompt).strip()

fromaddr = config['login']['user']
toaddrs  = prompt("To: ").split()
print("Enter message, end with ^D (Unix) or ^Z (Windows):")

# Add the From: and To: headers at the start!
msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs)))
while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    msg = msg + line

print("Message length is", len(msg))

server = smtplib.SMTP(config['server']['hostname'], config['server']['port'])
server.set_debuglevel(1)
server.starttls()
server.login(config['login']['user'], config['login']['password'])
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
