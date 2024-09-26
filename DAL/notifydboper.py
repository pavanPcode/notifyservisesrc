from HelperClass.sqlhelper import sqlhelper
from DAL.notifyqueries import *

def getemailaccount(superid,fromdb):
    try:
        qry = emailaccount.format(superid)
        runqry = sqlhelper(fromdb)
        rows = runqry.queryall(qry)
        if len(rows) == 0:
            return []
        return rows
    except Exception as e:
        return str(e)

def getemailqueue(noofrecs,fromdb):
    try:
        qry = emailqueue.format(noofrecs)
        runqry = sqlhelper(fromdb)
        rows = runqry.queryall(qry)
        if len(rows) == 0:
            return []
        return rows
    except Exception as e:
        return str(e)
def writeemailqueue(superid,toaddr,message,subject,fromdb):
    try:
        qry = insertmailqueue.format(superid,toaddr,subject,message)
        runqry = sqlhelper(fromdb)
        rows = runqry.update(qry)
        return rows
    except Exception as e:
        return {'status': False, 'message': str(e), "ResultData": []}

def updatequeueresponse(tablids,fromdb):
    try:
        # getting the comma-separated string from the list
        updtIds = ','.join(map(str, tablids)) 
        qry = updatemailqueue.format(updtIds)
        runqry = sqlhelper(fromdb)
        rows = runqry.update(qry)
        return 'Updated Successfully'    
    except Exception as e:
        return str(e)

def getwhatsappaccount(superid,fromdb):
    try:
        qry = whatsappaccount.format(superid)
        runqry = sqlhelper(fromdb)
        rows = runqry.queryall(qry)
        if len(rows) == 0:
            return []
        return rows
    except Exception as e:
        return str(e)
    
def getsmsaccount(superid,fromdb):
    try:
        qry = smsaccount.format(superid)
        runqry = sqlhelper(fromdb)
        rows = runqry.queryall(qry)
        if len(rows) == 0:
            return []
        return rows
    except Exception as e:
        return str(e)