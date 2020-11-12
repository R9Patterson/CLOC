#!/usr/bin/env python3

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


import os

#Get user input for repo
print("Paste repo URL, and press ENTER:")
string = str(input())

#Cone the repo 
os.system('git clone --depth 1' + " "+ string + " "+ 'temp-cloc-clone')

#Get user input for desired csv name
print(" ")
print("Enter desired name for your .CSV, and press ENTER:")
strCSV = str(input())

#Run CLOC and output results to csv
os.system('cloc temp-cloc-clone --csv --out'+ " " +'"'+strCSV+'.csv"')
fileStr = strCSV+".csv"

#Remove the repo from local storage
os.system('rm -rf temp-cloc-clone')

emailfrom = "patapptech@gmail.com"
emailto = "patapptech@gmail.com"
fileToSend = fileStr
username = "patapptech@gmail.com"
password = "Test!0qp"

#Get user input for repo
print("Enter email subject text, and press ENTER:")
esub = str(input())


msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = esub
msg.preamble = esub

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()