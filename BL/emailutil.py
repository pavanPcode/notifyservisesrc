from flask import json
from Model import emailmodel,whatsappmodel,smsmodel
from HelperClass.mailer import send_email,send_whatsapp,send_sms,send_otp_sms
from DAL.notifydboper import *

class EmailUtil:

    def sendemail(self,requestdata,attachments=None):
        try :
            superid = requestdata['superid']
            toemail = requestdata.get('toaddr')
            message = requestdata['message']
            subject = requestdata['subject']

            # Check if 'cc' and 'bcc' are present in requestdata
            cc = requestdata.get('cc')
            bcc = requestdata.get('bcc')

            rows = getemailaccount(superid,'pcdbconn')
            #print(rows)
            if len(rows) == 0:
                return {'status':False,'message':'Check mail credentials or superid not found'}
            if not isinstance(rows, dict):
                return {'status':False,'message':'Something went wrong or more than one superid found in database '}
            emlMdl = EmailUtil.prepareemailacctobj(rows)
            emlMdl.subject = subject
            emlMdl.tomail = toemail
            emlMdl.message = message

            # Assign 'cc' and 'bcc' to emlMdl if they exist
            if cc:
                emlMdl.cc = cc
            if bcc:
                emlMdl.bcc = bcc
            print(emlMdl.cc)

            result = send_email(emlMdl,attachments)
            return result
        except Exception as e:
            return {'status': False, 'message': f'send_email error : {str(e)}'}



    def sendbulkemail(self,sendmailcnt):
        try:
            rows = getemailqueue(sendmailcnt,'pcdbconn')
            if len(rows) == 0:
                return {'status': False, 'message': ' no records found'}
            EmailQueueTblIds = []
            for eachmail in rows:
                emlMdl = EmailUtil.prepareemailacctobj(eachmail)
                emlMdl.subject = eachmail['Subject']
                emlMdl.tomail = eachmail['ToAddress']
                emlMdl.message = eachmail['Message']
                retobj = send_email(emlMdl)
                EmailQueueTblIds.append(eachmail['Id'])
            updatequeueresponse(EmailQueueTblIds,'pcdbconn')
            return {'status': True, 'message': 'Updated Successfully',"ResultData":EmailQueueTblIds}
        except Exception as e:
            return {'status': False, 'message': f'sendbulkmail error : {str(e)}'}
    
    def queuemails(self,requestdata):
        superid = requestdata['superid'] 
        toemail = requestdata['toaddr']
        message = requestdata['message']
        subject = requestdata['subject']
        retstr = writeemailqueue(superid,toemail,message,subject,'pcdbconn')
        return retstr
        
    def prepareemailacctobj(dbobj):
        emlMdl = emailmodel.EmailModel()
        emlMdl.emailserver = dbobj['Host']
        emlMdl.port = dbobj['Port']
        emlMdl.frommail = dbobj['FromMail']
        emlMdl.displayname = dbobj['DisplayName']
        emlMdl.username = dbobj['UserName']
        emlMdl.password = dbobj['Password']
        return emlMdl
        
    def sendwhatsapp(self,requestdata):
        superid = requestdata['superid'] 
        tomobile = requestdata['tomobile']
        message = requestdata['message']
        rows = getwhatsappaccount(superid,'pcdbconn')
        if len(rows) == 0:
            return {'status': False, 'message': 'check whatsup credentials in db', 'ResultData': []}
        
        wamobj = whatsappmodel.WhatsappModel()
        wamobj.apikey = rows['APIKey']
        wamobj.mobile = tomobile
        wamobj.msg = message
        
        return send_whatsapp(rows["HostUrl"],wamobj)
        
    def sendsms(self,requestdata):
        superid = requestdata['superid'] 
        tomobile = requestdata['tomobile']
        message = requestdata['message']
        rows = getsmsaccount(superid,'pcdbconn')
        if len(rows) == 0:
            return []
        smsobj = smsmodel.SMSModel()
        smsobj.url = rows['APIUrl']
        smsobj.apikey = rows['APIKey']
        smsobj.senderid = rows['SenderId']
        smsobj.username = rows['UserName']
        smsobj.receipient = tomobile
        smsobj.message = message

        return send_sms(smsobj)

    def sendotpsms(self, requestdata):
        superid = requestdata['superid']
        tomobile = requestdata['tomobile']
        #message = requestdata['message']
        sendername = requestdata['sendername']
        otp = requestdata['otp']
        fromorg = requestdata['fromorg']
        rows = getsmsaccount(superid, 'pcdbconn')
        if len(rows) == 0:
            return {'status':False,'message':'No Sms records  in db',"ResultData":''}
        smsobj = smsmodel.SMSModel()
        smsobj.url = rows['APIUrl']
        smsobj.apikey = rows['APIKey']
        smsobj.senderid = rows['SenderId']
        smsobj.username = rows['UserName']
        smsobj.receipient = tomobile
        #smsobj.message = message
        smsobj.sendername = sendername
        smsobj.otp = otp
        smsobj.fromorg = fromorg

        return send_otp_sms(smsobj)
        
        