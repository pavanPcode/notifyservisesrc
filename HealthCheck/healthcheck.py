from .mysqlhelper import update_insert
from datetime import datetime, timedelta

def Healthchecklog(requestdata,rows,api,type):
    try:
        current_utc_time = datetime.utcnow()

        # Add 5 hours and 30 minutes
        time_difference = timedelta(hours=5, minutes=30)
        new_time = current_utc_time + time_difference

        if type == 1 or type == 2 :
            superid = requestdata['superid']
            toemail = requestdata['toaddr']
            message = requestdata['message']
            subject = requestdata['subject']
            status = rows['status']
            resmessage = rows['message']


            query = f"""INSERT INTO MailLog (superid, toaddr, Mailmessage, subject, Status, message,Service,type,createdon) VALUES 
                    ({superid}, '{toemail}', '{message}', '{subject}', '{status}', "{resmessage}",'{api}',{type},'{new_time}')"""

        if type == 3:
            superid = requestdata['superid']
            #toemail = requestdata['toaddr']
            toemail = requestdata.get('toemail')
            message = requestdata['message']
            subject = requestdata['subject']
            status = rows['status']
            resmessage = rows['message']
            #cc = requestdata.get('cc')
            bcc = requestdata.get('bcc')

            query = f"""INSERT INTO MailLog (superid, toaddr, Mailmessage, subject, Status, message,Service,type,bcc,createdon) VALUES 
                    ({superid}, '{toemail}', '{message}', '{subject}', '{status}', "{resmessage}",'{api}',{type},'{bcc}','{new_time}')"""

        elif type == 4:
            superid = requestdata['superid']
            tomobile = requestdata['tomobile']
            message = requestdata['message']
            status = rows['status']
            resmessage = rows['message']

            query = f"""INSERT INTO MailLog (superid, toaddr, Mailmessage, Status, message,Service,type,createdon) VALUES 
                            ({superid}, '{tomobile}', '{message}', '{status}', "{resmessage}",'{api}',{type},'{new_time}')"""


        result = update_insert(query)
        return result

    except Exception as e:
        print(e)
        return {'status': False, 'message': f"Error sending email: {e}"}