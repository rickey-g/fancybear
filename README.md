# Fancy Bear Source Code 
This repo contains actual source code found during IR.
The code provides a communication channel for the attacker and infected client. It uses Google's gmail servers to send and receive encoded messages.

### Some artifacts are summorized below
- Comments are in english, with a lot of grammar mistakes
- Subject of an email is: '**piradi nomeri**'. This means Personal Number in Georgian
- It saves files with **detaluri_**timetsamp.dat. 'Detaluri' is also Georgian for "details".
- In the email body it uses the word: "**gamarjoba**". Meaning 'Hello' in  Georgian.


### These are the Gmail account details used, I've verified they once worked (but not anymore!)
- POP3_MAIL_IP = 'pop.gmail.com'  
- POP3_PORT = 995
- POP3_ADDR = 'jassnovember30@gmail.com'
- POP3_PASS = '30Jass11'
- SMTP_MAIL_IP = 'smtp.gmail.com'
- SMTP_PORT = 587
- SMTP_TO_ADDR = 'userdf783@mailtransition.com'
- SMTP_FROM_ADDR = 'ginabetz75@gmail.com'
- SMTP_PASS = '75Gina75'
  
### Command and Control server
- XAS_IP = '104.152.187.66'
- XAS_GATE = '/updates/'

**The code is completely left as found on the original server, including the log files.**

**ESET** has the complete source code of XAgent, read their report here:
http://www.welivesecurity.com/wp-content/uploads/2016/10/eset-sednit-part-2.pdf
