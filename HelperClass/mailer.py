import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import os

def send_sms(smsdata):
    try:
        url = smsdata.url
        url = url.replace('#USERNAME#',smsdata.username)
        url = url.replace('#APIKEYVAR#',smsdata.apikey)
        url = url.replace('#SENDERIDVAR#',smsdata.senderid)
        url = url.replace('#SENDNOVAR#',str(smsdata.receipient))
        url = url.replace('#SENDMSGVAR#',smsdata.message  )
        res = requests.get(url)
        return {}
    except Exception as e:
        print(str(e),99)
        return False

def send_otp_sms(smsdata):
    try:
        url = smsdata.url
        url = url.replace('#USERNAME#',smsdata.username)
        url = url.replace('#APIKEYVAR#',smsdata.apikey)
        url = url.replace('#SENDERIDVAR#',smsdata.senderid)
        url = url.replace('#SENDNOVAR#',str(smsdata.receipient))
        print(smsdata.sendername,smsdata.otp,smsdata.fromorg)
        message = """Dear {0} Your login OTP is {1}.{2} PERENNIAL CODE""".format(smsdata.sendername,smsdata.otp,smsdata.fromorg)
        print(message)
        url = url.replace('#SENDMSGVAR#',message)

        res = requests.get(url)

        return {'status':True,'message':'opt succ',"ResultData":str(res.text)}

    except Exception as e:
        return {'status':False,'message':f'send_email error : {str(e)}',"ResultData":''}


def send_whatsapp(url,whatsappdata):
    try:
        whatsapirequest = {'apikey': whatsappdata.apikey, 'mobile': whatsappdata.mobile,'msg': whatsappdata.msg }
        res = requests.post(url=url, params=whatsapirequest)
        result = res.json()
        if result['status'] == 'success':
            return {'status': True, 'message': result, 'ResultData': []}
        else:
            return {'status': False, 'message': result, 'ResultData': []}
    except Exception as e:
        return {'status': False, 'message': str(e.message), 'ResultData': []}
    
def send_email(emailObj,attachments=None):
    try:
        sender_email = emailObj.frommail
        password = emailObj.password
        smtp_server = emailObj.emailserver
        smtp_port = emailObj.port

        msg = MIMEMultipart()
        msg["Subject"] = emailObj.subject
        msg["From"] = emailObj.frommail 
        msg["To"] = emailObj.tomail

        if emailObj.bcc:
            #msg['Bcc']  = emailObj.bcc
            bcc_emails = emailObj.bcc.split(',')
        else:
            bcc_emails = []

        if emailObj.cc:
            msg['Cc'] = emailObj.cc
            cc_emails = emailObj.cc.split(',')
        else:
            cc_emails = []


        html_message = emailObj.message

        if html_message:
            # Create an HTML part of the message
            html_part = MIMEText(html_message, "html")
            msg.attach(html_part)

        #for attachments only
        if attachments:
            attachment_paths = []

            # Check if /tmp directory exists, create it if not
            if not os.path.exists("/tmp"):
                os.makedirs("/tmp")

            for attachment in attachments:
                attachment_path = f"/tmp/{attachment.filename}"  # Save the attachment temporarily
                #print(attachment_path)
                attachment.save(attachment_path)
                attachment_paths.append(attachment_path)
                with open(attachment_path, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachment.filename}",
                )
                msg.attach(part)
        try:
            # Establish a secure SMTP connection
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(sender_email, password)

                if emailObj.bcc:
                    mailids = bcc_emails
                else :
                    recipients = emailObj.tomail.split(',')
                    mailids = recipients +  cc_emails

                server.sendmail(sender_email, mailids, msg.as_string())
        except smtplib.SMTPException as e:
            return {'status': False, 'message': f"Error sending email: {e}"}
        except Exception as e:
            return {'status': False, 'message': f"Error sending email: {e}"}

        if attachments:
            # Clean up temporary attachment files
            for attachment_path in attachment_paths:
                os.remove(attachment_path)

        return {'status':True,'message':'send_email succ'}
    except Exception as e:
        return {'status':False,'message':f'send_email error : {str(e)}'}
