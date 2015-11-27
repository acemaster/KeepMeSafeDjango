import smtplib
import socks

#socks.setdefaultproxy(TYPE, ADDR, PORT)
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '172.30.0.7', 3128)
socks.wrapmodule(smtplib)

smtpserver = 'smtp.gmail.com'
AUTHREQUIRED = 1 
smtpuser = 'vivekhtc25@hotmail.fr'  
smtppass = '3l3m3nts'  

RECIPIENTS = 'vivekhtc25@gmail.com'
SENDER = 'vivekhtc25@gmail.com'
mssg = "test message"
s = mssg   

server = smtplib.SMTP(smtpserver,587)
server.ehlo()
server.starttls() 
server.ehlo()
server.login(smtpuser,smtppass)
server.set_debuglevel(1)
server.sendmail(SENDER, [RECIPIENTS], s)
server.quit()