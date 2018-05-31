#coding=utf-8
import os, random, datetime, re
import smtplib
from email.Header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from myapi import db, app
from myapi.model.smtp import EmailModel
from flask import jsonify
from flask.ext.restful import Resource, reqparse

class sendEmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recivers', type=str, location='json', required=True)
        parser.add_argument('folderName', type=str, location='json', required=True)
        args = parser.parse_args()
        return jsonify(result=send(args.recivers.split(','), args.folderName))

mail_host = "smtp.qq.com"
mail_user = "huoapeng"
mail_pass = "fzrnghnaqnicbidh"
mail_postfix = "qq.com"
mail_from = "聚形科技<{}@{}>".format(mail_user, mail_postfix)
def send(recivers, folderName):
    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = mail_from
    filePath = os.path.join(app.config['ROOT_PATH'], app.config['EMAIL_FOLDER'], folderName)


    for reciver in recivers:
        with open(filePath+'/subject.txt', 'rt') as f:
            data = f.read()
            msgRoot['Subject'] = data#Header(data,'utf-8')  

        # msgRoot['To'] = ";".join(recivers)
        # msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        # msgText = MIMEText('This is the alternative plain text message.', _subtype='plain', _charset='utf-8')
        # msgAlternative.attach(msgText)

        params = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ', 13))
        with open(filePath+'/content.html', 'rt') as f:
            data = f.read()
            msgText = MIMEText(data.replace('!#1800#!', params).replace('!#email#!', reciver)
             , _subtype='html', _charset='utf-8')
            msgAlternative.attach(msgText)

        imgPath = filePath+'/img/'
        for fname in os.listdir(imgPath):
            if os.path.isfile(os.path.join(imgPath, fname)):
                fp = open(os.path.join(imgPath, fname), 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                msgImage.add_header('Content-ID', '<{}>'.format(fname.rsplit('.', 1)[0]))
                msgRoot.attach(msgImage)
        
        try:
            server = smtplib.SMTP()
            server.connect(mail_host, 587)
            server.ehlo()
            server.starttls()
            server.login(mail_user, mail_pass)
            msgRoot['To'] = reciver
            server.sendmail(mail_from, reciver, msgRoot.as_string())

            e = EmailModel(reciver, params, datetime.datetime.now() + datetime.timedelta(seconds=1800))
            db.session.add(e)
            db.session.commit()
            server.quit()
            server.close()
            return True
        except Exception, e:
            # print str(e)
            return str(e)


