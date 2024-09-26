from flask import Flask, jsonify,request,Blueprint
from BL import emailutil
from HealthCheck.healthcheck import Healthchecklog
import threading
import time
notifyservice = Blueprint('notifyservice',__name__, url_prefix='/notify')


def write_log(inputdata,rows,api,type):
    try:
        # Create a thread for maillog execution
        thread = threading.Thread(target=Healthchecklog, args=(inputdata, rows,api,type))
        thread.start()
    except Exception as e:
        result = {"status": False, "message": f"Unexpected error: {e}"}
        thread = threading.Thread(target=Healthchecklog, args=(inputdata, result,api,type))
        thread.start()


@notifyservice.route('/sendmail', methods=['POST'])
def senddirectemail():
    try :
        if request.method == 'POST':
            inputdata = request.json
            emlUtil = emailutil.EmailUtil()
            rows = emlUtil.sendemail(inputdata)
            #writing healthcheck
            try:
                write_log(inputdata, rows, 'sendmail', 1)
            except Exception as e:
                pass

            if rows['status'] == True:
                return jsonify(rows) ,200
            return jsonify(rows)
    except Exception as e:
        rows = {'status': False, 'message': f'send_email error : {str(e)}'}
        ####writing healthcheck
        try:
            write_log(inputdata, rows, 'sendmail', 1)
        except Exception as e:
            pass
        return {'status': False, 'message': f'send_email error : {str(e)}'}

@notifyservice.route('/sendmailattachments', methods=['POST'])
def sendmailattachments():
    try:
        if request.method == 'POST':
            inputdata = request.form
            attachments = request.files.getlist('attachments')
            emlUtil = emailutil.EmailUtil()
            rows = emlUtil.sendemail(inputdata,attachments)

            ####writing healthcheck
            try:
                write_log(inputdata, rows,'sendmailattachments',2)
            except Exception as e:
                pass

            if rows['status'] == True:
                return jsonify(rows) ,200
            return jsonify(rows)
    except Exception as e:
        rows = {'status': False, 'message': f'send_email error : {str(e)}'}
        ####writing healthcheck
        try:
            write_log(inputdata, rows,'sendmailattachments',2)
        except Exception as e:
            pass
        return {'status': False, 'message': f'send_email error : {str(e)}'}

@notifyservice.route('/sendMailWithBcc', methods=['POST'])
def sendMailWithRecipients():
    try:
        if request.method == 'POST':
            inputdata = request.form
            attachments = request.files.getlist('attachments')
            emlUtil = emailutil.EmailUtil()
            rows = emlUtil.sendemail(inputdata,attachments)

            ####writing healthcheck
            try:
                write_log(inputdata, rows,'sendMailWithRecipients',3)
            except Exception as e:
                pass

            if rows['status'] == True:
                return jsonify(rows) ,200
            return jsonify(rows)
    except Exception as e:
        rows = {'status': False, 'message': f'send_email error : {str(e)}'}
        ####writing healthcheck
        try:
            write_log(inputdata, rows,'sendMailWithRecipients',3)
        except Exception as e:
            pass
        return {'status': False, 'message': f'send_email error : {str(e)}'}


@notifyservice.route('/queuemail', methods=['POST'])
def sendemaillater():
    if request.method == 'POST':
        inputdata = request.json
        emlUtil = emailutil.EmailUtil()
        rows = emlUtil.queuemails(inputdata)
        return jsonify(rows)


@notifyservice.route('/bulkemail')
def sendbulkmail():
    try:
        noofrecords = request.args.get('reccnt')
        emlUtil = emailutil.EmailUtil()
        rows = emlUtil.sendbulkemail(noofrecords)
        return jsonify(rows)
    except Exception as e:
        return {'status': False, 'message': f'sendbulkmail error : {str(e)}'}


@notifyservice.route('/sendwhatsapp', methods=['POST'])
def senddirectwhatsapp():
    if request.method == 'POST':
        inputdata = request.json
        emlUtil = emailutil.EmailUtil()
        rows = emlUtil.sendwhatsapp(inputdata)

        ####writing healthcheck
        try:
            write_log(inputdata, rows, 'sendwhatsapp', 4)
        except Exception as e:
            pass

        return jsonify(rows)
    #     if len(rows) == 0:
    #         return jsonify(status=False,message='No Records')
    # return jsonify(status=True,message='success')

@notifyservice.route('/queuewhatsapp', methods=['POST'])
def sendwhatsapplater():
    if request.method == 'POST':
        inputdata = request.json
        emlUtil = emailutil.EmailUtil()
        rows = emlUtil.queuemails(inputdata)
    return jsonify(status='success')

@notifyservice.route('/sendsms', methods=['POST'])
def senddirectsms():
    if request.method == 'POST':
        inputdata = request.json
        emlUtil = emailutil.EmailUtil()
        rows = emlUtil.sendsms(inputdata)
        if rows == False:
            return jsonify(status='No Records')
    return jsonify(status='success')

@notifyservice.route('/sendotpsms', methods=['POST'])
def sendotpsms():
    if request.method == 'POST':
        inputdata = request.json
        emlUtil = emailutil.EmailUtil()
        rows = emlUtil.sendotpsms(inputdata)
        return jsonify(rows)