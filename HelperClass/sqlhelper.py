import configparser
import pyodbc

class sqlhelper():
    global dbinfo,config
    CONFIG_PATH = '/dbConfig.ini'  
    config = configparser.ConfigParser()
    config.read('dbConfig.ini')
    dbinfo = "DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={0};PORT=1433;DATABASE={1};UID={2};PWD={3}"
    
    """ Collection of helper methods to query the MS SQL Server database.
    """
    def __init__(self,dbname):
        self.connstr = dbinfo.format(config.get(dbname,"host"),config.get(dbname,"database"),config.get(dbname,"user"),config.get(dbname,"password"))
        #self.dbconn = pyodbc.connect(conn)
    
    def dbconnect(self):
        self.dbconn = pyodbc.connect(self.connstr)
        return self.dbconn.cursor()  
    
    def disconnect(self):
        if self.dbconn:
            self.dbconn.close()  

    def queryall(self,sqlqry):
        try:
            cursor = self.dbconnect()
            cursor.execute(sqlqry)
            result = self.getdictobj(cursor)
            self.disconnect()
            return result
        except Exception as e:
            self.disconnect()
            print(f"Error executing query: {e}")
            return []
    
    def update(self,sqlqry):
        try:
            cursor = self.dbconnect() 
            cursor.execute(sqlqry)
            cursor.commit()
            self.disconnect()
            #return 1
            return {'status': True, 'message': 'Updated Successfully', "ResultData": []}
        except Exception as e:
            self.disconnect()
            print(f"Error executing query: {e}")
            #return 0
            return {'status': False, 'message': str(e), "ResultData": []}

    def rows(self):
        cursor = self.dbconnect() 
        return cursor.rowcount

    def execstoredproc(self,query):
        try:
            cursor = self.dbconnect() 
            cursor.execute(query)
            result = self.getdictobj(cursor)
            self.disconnect()
            return result
        except Exception as e:
            self.disconnect()
            print(e)
            return []
        
    def execstoreproc(self,query):
        try:
            result = []
            cursor = self.dbconnect() 
            cursor.execute(query)
            # Check the description attribute
            descriptions = cursor.description
            if descriptions is not None:
                # If there are multiple result sets, descriptions will be a list of tuples
                if isinstance(descriptions, list):
                    for result_set in cursor:
                        retrow = self.getdictobj(result_set)
                        result.append(retrow)
                # If there's only one result set, descriptions will be a tuple
                elif isinstance(descriptions, tuple):
                    rows = self.getdictobj(cursor)
                    if not rows:
                        result = []
                    result.append(rows)
            self.dbclose()
            return result
        except Exception as e:
            print(e)
            return []
        
    def getdictobj(self,cursor):
        # Get column names from the description attribute
        columns = [column[0] for column in cursor.description]
        # Fetch all rows
        rows = cursor.fetchall()
        print(rows)
        if rows:
            if len(rows) == 1:
                row_dict = dict(zip(columns, rows[0]))
            elif len(rows) > 1 :
                row_dict = [dict(zip(columns, row)) for row in rows]
            else:
                row_dict = []
        else:
            row_dict = []
        return row_dict