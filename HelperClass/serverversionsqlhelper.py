#this file is server version as db connection is different

import configparser
#from contextlib import contextmanager
import os
import pyodbc
#import sys

class sqlhelper():
    global dbinfo,config
    os.environ["ODBCSYSINI"] = "/home/code9"

    CONFIG_PATH = '/dbconfig.ini'
    config = configparser.ConfigParser()
    config.read('/home/code9/pcapi/dbconfig.ini')


    """ Collection of helper methods to query the MS SQL Server database.
    """
    def __init__(self,dbname):
        dbinfo = 'DSN=primesqlserverdatasource;DATABASE={0};UID={1};PWD={2};Encrypt=yes;'
        if dbname == 'primedbconn':
            dbinfo = 'DSN=primesqlserverdatasource;DATABASE={0};UID={1};PWD={2};Encrypt=yes;'
        else:
            dbinfo = 'DSN=pcsqlserverdatasource;DATABASE={0};UID={1};PWD={2};Encrypt=yes;'
        self.connstr = dbinfo.format(config.get(dbname,"database"),config.get(dbname,"user"),config.get(dbname,"password"))
        

    def dbconnect(self):
        self.dbconn = pyodbc.connect(self.connstr)
        return self.dbconn.cursor()  
    
    def dbclose(self):
        self.dbconn.close()  

    def convertrowtodict(self,rows):
        try:
            if rows == None:
                return []
            elif len(rows) == 0:
                return []
            return [dict(zip([column[0] for column in rows.description], row)) for row in rows.fetchall()]
        except Exception as e:
            return []
        
    def queryall(self,sqlqry):
        cursor = self.dbconnect()
        cursor.execute(sqlqry)
        rows = cursor.fetchall()
        self.dbclose()
        return self.convertrowtodict(rows)
    
    def queryone(self,sqlqry):
        cursor = self.dbconnect() 
        cursor.execute(sqlqry)
        rows = cursor.fetchone()
        self.dbclose()
        return self.convertrowtodict(rows)
        
    
    def update(self,sqlqry):
        cursor = self.dbconnect() 
        cursor.execute(sqlqry)
        cursor.commit()
        self.dbclose()
        return 1

    def rows(self):
        cursor = self.dbconnect() 
        return cursor.rowcount
