from HelperClass.dataoutputmodel import DataOutputModel
from datetime import datetime
import datetime as dt
class commonutil:
    def InvalidResult(self,Message) :
        return DataOutputModel(Message,[],False)
    
    def SuccessResult(self,Message) :
        return DataOutputModel(Message,[],True)
    
    def ValidateLicense(self,gen_key,superid):
        dt = self.extract_date_from_key(gen_key)
        
        try:
             # Compare the expiry date with the current date
            n_days = (dt - datetime.now()).days
            n_place = 4
            tempsuperid = int(gen_key[n_place - 1:n_place + 4])
            if n_days > 0 and tempsuperid == superid:
                return True, n_days
            else:
                return False, 0
        except ValueError:
            return False, 0
            # Handle the case where the extracted values result in an invalid datetime
            #return DataOutputModel("Invalid License",[],False)

        
    def extract_date_from_key(self,gen_key):
        # Extracting values from specific positions in the GenKey string
        licnum = gen_key[2]
        n_place = 11
        month = int(gen_key[n_place - 1:n_place + 1]) - 10

        n_place = 27
        year = int(gen_key[n_place - 1:n_place + 1]) + 2000

        n_place = 34
        day = int(gen_key[n_place - 1:n_place + 1]) - 10
        # Constructing a datetime object
        expiry_date = dt.datetime(year, month, day)
        return expiry_date

    
