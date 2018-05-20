# -*- coding: utf-8 -*- 


import sys
import requests
import smtplib
import hashlib
import Main
import os

previos_query=u"Virginia Woolf’s 136th birthday"
GMAIL_USERNAME='vignanstudent@gmail.com'
GMAIL_PASSWORD='07Dell590'
TO = 'dhatric@gmail.com'


def SendMail(str):
    email_subject="New Doodle Added" + str
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    headers = "\r\n".join(["from: " + GMAIL_USERNAME, "subject: " + email_subject,"to: " + TO,"mime-version: 1.0","content-type: text/html"])
    print str
    content = headers + "\r\n\r\n" + str
    return session.sendmail(GMAIL_USERNAME, TO, content)


if __name__ == '__main__':
    print 'checking'
    #os.chdir('C:\\Giridhar\\Projects\\python\\Doodles\\RandomProject\\com\\doodles\\video')
    URL='https://www.google.com/doodles/json/2018/5'
    PARAMS = {'hl':'en_GB'}
    request = requests.get(url = URL, params = PARAMS)
    data = request.json()
    doodleJson = None
    doodleJson=data[0]
    file_read = open("LastSuccess.txt", "r") 
    file_content = hashlib.md5(file_read.read()).hexdigest()
    file_read.close()
    doole_content= hashlib.md5(doodleJson['name']).hexdigest()
    if doole_content != file_content:
        print "change found"
        SendMail(doodleJson['name'])
        Main.autoPlayDoodle(doodleJson)
        
        